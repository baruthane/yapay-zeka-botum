"""
Order Book analysis module
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from utils.logger import get_logger

logger = get_logger(__name__)

class OrderBookAnalyzer:
    """Analyze order book metrics"""
    
    @staticmethod
    def calculate_order_book_imbalance(order_book: Dict) -> float:
        """
        Calculate Order Book Imbalance (OBI)
        
        OBI = (BidVolume - AskVolume) / (BidVolume + AskVolume)
        
        Range: -1 to +1
        Positive = Bullish (more buy pressure)
        Negative = Bearish (more sell pressure)
        """
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                return 0.0
            
            bid_volume = sum(bid['quantity'] for bid in bids)
            ask_volume = sum(ask['quantity'] for ask in asks)
            
            total_volume = bid_volume + ask_volume
            
            if total_volume == 0:
                return 0.0
            
            obi = (bid_volume - ask_volume) / total_volume
            return float(np.clip(obi, -1, 1))
        
        except Exception as e:
            logger.error(f"Error calculating OBI: {e}")
            return 0.0
    
    @staticmethod
    def calculate_spread(order_book: Dict) -> float:
        """
        Calculate bid-ask spread
        Spread = Ask₁ - Bid₁
        """
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                return 0.0
            
            bid_price = float(bids[0]['price'])
            ask_price = float(asks[0]['price'])
            
            spread = ask_price - bid_price
            return float(spread)
        
        except Exception as e:
            logger.error(f"Error calculating spread: {e}")
            return 0.0
    
    @staticmethod
    def calculate_spread_percentage(order_book: Dict) -> float:
        """Calculate spread as percentage of mid price"""
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                return 0.0
            
            bid_price = float(bids[0]['price'])
            ask_price = float(asks[0]['price'])
            mid_price = (bid_price + ask_price) / 2
            
            if mid_price == 0:
                return 0.0
            
            spread_pct = ((ask_price - bid_price) / mid_price) * 100
            return float(spread_pct)
        
        except Exception as e:
            logger.error(f"Error calculating spread %: {e}")
            return 0.0
    
    @staticmethod
    def get_depth_analysis(order_book: Dict, levels: int = 10) -> Dict:
        """
        Analyze order book depth at different levels
        """
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            bid_depth = sum(bid['quantity'] for bid in bids[:levels])
            ask_depth = sum(ask['quantity'] for ask in asks[:levels])
            
            return {
                'bid_depth': float(bid_depth),
                'ask_depth': float(ask_depth),
                'depth_imbalance': (bid_depth - ask_depth) / (bid_depth + ask_depth) if (bid_depth + ask_depth) > 0 else 0,
                'total_depth': float(bid_depth + ask_depth)
            }
        
        except Exception as e:
            logger.error(f"Error calculating depth analysis: {e}")
            return {'bid_depth': 0, 'ask_depth': 0, 'depth_imbalance': 0, 'total_depth': 0}
    
    @staticmethod
    def get_volume_profile(order_book: Dict) -> Dict:
        """Get volume distribution profile"""
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            bid_volume = sum(bid['quantity'] for bid in bids)
            ask_volume = sum(ask['quantity'] for ask in asks)
            
            return {
                'total_bid_volume': float(bid_volume),
                'total_ask_volume': float(ask_volume),
                'volume_ratio': float(bid_volume / ask_volume) if ask_volume > 0 else 0,
                'dominance': 'BUY' if bid_volume > ask_volume else 'SELL'
            }
        
        except Exception as e:
            logger.error(f"Error calculating volume profile: {e}")
            return {'total_bid_volume': 0, 'total_ask_volume': 0, 'volume_ratio': 0, 'dominance': 'NEUTRAL'}
    
    @staticmethod
    def detect_order_wall(order_book: Dict, threshold_multiplier: float = 2.0) -> Dict:
        """
        Detect large orders (walls) in the order book
        threshold_multiplier: multiplier of average volume to detect a wall
        """
        try:
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                return {'bid_wall': None, 'ask_wall': None}
            
            # Calculate average volume
            bid_volumes = [bid['quantity'] for bid in bids]
            ask_volumes = [ask['quantity'] for ask in asks]
            
            avg_bid = np.mean(bid_volumes)
            avg_ask = np.mean(ask_volumes)
            
            # Find largest bids and asks
            bid_wall = None
            ask_wall = None
            
            for bid in bids:
                if bid['quantity'] > avg_bid * threshold_multiplier:
                    bid_wall = {'price': float(bid['price']), 'quantity': float(bid['quantity'])}
                    break
            
            for ask in asks:
                if ask['quantity'] > avg_ask * threshold_multiplier:
                    ask_wall = {'price': float(ask['price']), 'quantity': float(ask['quantity'])}
                    break
            
            return {'bid_wall': bid_wall, 'ask_wall': ask_wall}
        
        except Exception as e:
            logger.error(f"Error detecting order walls: {e}")
            return {'bid_wall': None, 'ask_wall': None}
    
    @staticmethod
    def analyze_full_order_book(order_book: Dict) -> Dict:
        """Comprehensive order book analysis"""
        try:
            analysis = {
                'obi': OrderBookAnalyzer.calculate_order_book_imbalance(order_book),
                'spread': OrderBookAnalyzer.calculate_spread(order_book),
                'spread_pct': OrderBookAnalyzer.calculate_spread_percentage(order_book),
                'depth': OrderBookAnalyzer.get_depth_analysis(order_book),
                'volume_profile': OrderBookAnalyzer.get_volume_profile(order_book),
                'order_walls': OrderBookAnalyzer.detect_order_wall(order_book),
                'timestamp': order_book.get('timestamp')
            }
            return analysis
        except Exception as e:
            logger.error(f"Error in full order book analysis: {e}")
            return {}
