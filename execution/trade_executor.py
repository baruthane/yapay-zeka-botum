"""
Trade executor module
"""
from data_collector.binance_client import BinanceClient
from risk_management.risk_manager import RiskManager
from utils.logger import get_logger
from typing import Dict, Optional
from datetime import datetime

logger = get_logger(__name__)

class TradeExecutor:
    """Execute trades based on signals"""
    
    def __init__(self, binance_client: BinanceClient, risk_manager: RiskManager):
        """
        Initialize trade executor
        
        Args:
            binance_client: Binance API client
            risk_manager: Risk management instance
        """
        self.client = binance_client
        self.risk_manager = risk_manager
        self.executed_trades = []
    
    def execute_long_trade(self, symbol: str, quantity: float, entry_price: float,
                          stop_loss: float, take_profit: float,
                          signal_score: float, confidence: float) -> Dict:
        """
        Execute a LONG trade
        
        Args:
            symbol: Trading pair
            quantity: Position size
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            signal_score: Trading signal score (0-100)
            confidence: Confidence level (0-1)
            
        Returns:
            Trade execution result
        """
        try:
            logger.info(f"Executing LONG trade: {symbol} {quantity} @ {entry_price}")
            
            # Place market buy order
            order = self.client.place_market_order(symbol, quantity, 'BUY')
            
            if not order:
                logger.error(f"Failed to place buy order for {symbol}")
                return {'success': False, 'error': 'Failed to place order'}
            
            order_id = order.get('orderId')
            
            # Place stop loss order
            sl_order = self.client.place_stop_loss_order(symbol, quantity, stop_loss, 'SELL')
            
            # Place take profit order
            tp_order = self.client.place_limit_order(symbol, quantity, take_profit, 'SELL')
            
            trade_record = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'direction': 'LONG',
                'quantity': quantity,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'signal_score': signal_score,
                'confidence': confidence,
                'order_id': order_id,
                'sl_order_id': sl_order.get('orderId') if sl_order else None,
                'tp_order_id': tp_order.get('orderId') if tp_order else None,
                'status': 'OPEN'
            }
            
            self.executed_trades.append(trade_record)
            
            logger.info(f"LONG trade executed successfully: {order_id}")
            return {
                'success': True,
                'trade': trade_record
            }
        
        except Exception as e:
            logger.error(f"Error executing LONG trade: {e}")
            return {'success': False, 'error': str(e)}
    
    def execute_short_trade(self, symbol: str, quantity: float, entry_price: float,
                           stop_loss: float, take_profit: float,
                           signal_score: float, confidence: float) -> Dict:
        """
        Execute a SHORT trade
        
        Args:
            symbol: Trading pair
            quantity: Position size
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            signal_score: Trading signal score (0-100)
            confidence: Confidence level (0-1)
            
        Returns:
            Trade execution result
        """
        try:
            logger.info(f"Executing SHORT trade: {symbol} {quantity} @ {entry_price}")
            
            # Place market sell order
            order = self.client.place_market_order(symbol, quantity, 'SELL')
            
            if not order:
                logger.error(f"Failed to place sell order for {symbol}")
                return {'success': False, 'error': 'Failed to place order'}
            
            order_id = order.get('orderId')
            
            # Place stop loss order
            sl_order = self.client.place_stop_loss_order(symbol, quantity, stop_loss, 'BUY')
            
            # Place take profit order
            tp_order = self.client.place_limit_order(symbol, quantity, take_profit, 'BUY')
            
            trade_record = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'direction': 'SHORT',
                'quantity': quantity,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'signal_score': signal_score,
                'confidence': confidence,
                'order_id': order_id,
                'sl_order_id': sl_order.get('orderId') if sl_order else None,
                'tp_order_id': tp_order.get('orderId') if tp_order else None,
                'status': 'OPEN'
            }
            
            self.executed_trades.append(trade_record)
            
            logger.info(f"SHORT trade executed successfully: {order_id}")
            return {
                'success': True,
                'trade': trade_record
            }
        
        except Exception as e:
            logger.error(f"Error executing SHORT trade: {e}")
            return {'success': False, 'error': str(e)}
    
    def execute_signal(self, symbol: str, signal: str, score: float, 
                      confidence: float, entry_price: float, atr: float) -> Dict:
        """
        Execute trade based on signal
        
        Args:
            symbol: Trading pair
            signal: 'LONG', 'SHORT', or 'WAIT'
            score: Signal score (0-100)
            confidence: Confidence level (0-1)
            entry_price: Current price
            atr: ATR for stop loss calculation
            
        Returns:
            Execution result
        """
        try:
            # Check if we can open position
            open_positions = self.client.get_open_positions()
            if not self.risk_manager.can_open_position(len(open_positions)):
                logger.warning("Cannot open position due to risk limits")
                return {'success': False, 'error': 'Risk limits exceeded'}
            
            if signal == 'WAIT':
                return {'success': True, 'signal': 'WAIT', 'message': 'Waiting for better entry'}
            
            # Calculate stop loss and take profit
            if signal == 'LONG':
                stop_loss = self.risk_manager.calculate_stop_loss_atr(entry_price, atr, 'LONG')
                take_profit = self.risk_manager.calculate_take_profit(entry_price, stop_loss, 2.0, 'LONG')
                quantity = self.risk_manager.calculate_position_size(entry_price, stop_loss)
                
                if quantity <= 0:
                    return {'success': False, 'error': 'Invalid position size'}
                
                return self.execute_long_trade(symbol, quantity, entry_price, stop_loss, 
                                              take_profit, score, confidence)
            
            elif signal == 'SHORT':
                stop_loss = self.risk_manager.calculate_stop_loss_atr(entry_price, atr, 'SHORT')
                take_profit = self.risk_manager.calculate_take_profit(entry_price, stop_loss, 2.0, 'SHORT')
                quantity = self.risk_manager.calculate_position_size(entry_price, stop_loss)
                
                if quantity <= 0:
                    return {'success': False, 'error': 'Invalid position size'}
                
                return self.execute_short_trade(symbol, quantity, entry_price, stop_loss,
                                               take_profit, score, confidence)
        
        except Exception as e:
            logger.error(f"Error executing signal: {e}")
            return {'success': False, 'error': str(e)}
    
    def close_position(self, symbol: str, direction: str) -> Dict:
        """Close an open position"""
        try:
            positions = self.client.get_open_positions()
            
            for pos in positions:
                if pos['symbol'] == symbol:
                    qty = abs(float(pos['quantity']))
                    
                    # Close with market order
                    if float(pos['quantity']) > 0:  # Long position
                        order = self.client.place_market_order(symbol, qty, 'SELL')
                    else:  # Short position
                        order = self.client.place_market_order(symbol, qty, 'BUY')
                    
                    logger.info(f"Position closed: {symbol} {qty}")
                    return {'success': True, 'order': order}
            
            return {'success': False, 'error': 'Position not found'}
        
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_trade_history(self, limit: int = 50) -> list:
        """Get recent trade history"""
        return self.executed_trades[-limit:]
