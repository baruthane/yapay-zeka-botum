"""
Flask webhook server for TradingView signals
"""
from flask import Flask, request, jsonify
import hmac
import hashlib
from bot import TradingBot
from utils.logger import get_logger
from config import WEBHOOK_PORT, WEBHOOK_SECRET
import threading

logger = get_logger(__name__)

app = Flask(__name__)
bot = TradingBot()

def verify_webhook(request_data: str, signature: str) -> bool:
    """Verify webhook signature"""
    try:
        expected_sig = hmac.new(
            WEBHOOK_SECRET.encode(),
            request_data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_sig)
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Receive TradingView webhook signals
    
    Expected JSON:
    {
        "symbol": "BTCUSDT",
        "signal": "LONG",
        "price": "105000"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract webhook data
        symbol = data.get('symbol', '').upper()
        signal = data.get('signal', '').upper()
        price = float(data.get('price', 0))
        
        logger.info(f"Webhook received: {symbol} {signal} @ {price}")
        
        # Validate signal
        if signal not in ['LONG', 'SHORT', 'EXIT_LONG', 'EXIT_SHORT']:
            return jsonify({'error': f'Invalid signal: {signal}'}), 400
        
        if not symbol or price <= 0:
            return jsonify({'error': 'Invalid symbol or price'}), 400
        
        # Handle signals in background thread
        if signal in ['LONG', 'SHORT']:
            thread = threading.Thread(
                target=bot.trade_executor.execute_signal,
                args=(symbol, signal, 0, 0, price, 0)
            )
            thread.daemon = True
            thread.start()
        
        elif signal == 'EXIT_LONG' or signal == 'EXIT_SHORT':
            thread = threading.Thread(
                target=bot.trade_executor.close_position,
                args=(symbol, signal)
            )
            thread.daemon = True
            thread.start()
        
        logger.info(f"Signal processed: {symbol} {signal}")
        
        return jsonify({
            'status': 'success',
            'symbol': symbol,
            'signal': signal,
            'price': price
        }), 200
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'bot': 'running'}), 200

@app.route('/status', methods=['GET'])
def status():
    """Get bot status"""
    try:
        risk_report = bot.get_risk_report()
        return jsonify({
            'status': 'ok',
            'risk_report': risk_report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signal/<symbol>', methods=['GET'])
def get_signal(symbol):
    """Get signal for a specific symbol"""
    try:
        symbol = symbol.upper()
        signal_data = bot.generate_signal(symbol)
        return jsonify({
            'symbol': symbol,
            'signal': signal_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info(f"Starting webhook server on port {WEBHOOK_PORT}")
    app.run(host='0.0.0.0', port=WEBHOOK_PORT, debug=False)
