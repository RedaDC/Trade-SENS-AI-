from models import UserChallenge, Trade
from extensions import db
from datetime import datetime

class ChallengeService:
    
    @staticmethod
    def process_trade_result(challenge_id: int, pnl: float):
        challenge = UserChallenge.query.get(challenge_id)
        if not challenge or challenge.status != 'ACTIVE':
            return
            
        # Update Balance/Equity
        challenge.current_equity += pnl
        
        # Check Rules
        ChallengeService.evaluate_rules(challenge)
        db.session.commit()

    @staticmethod
    def evaluate_rules(challenge: UserChallenge):
        # 1. Start of day balance logic would be needed for Daily Loss, 
        # for simplicity assuming daily_max_loss is absolute from initial for this MVP 
        # or we need to track start_of_day_equity in DB.
        
        # Drawdown calculation
        drawdown = challenge.initial_balance - challenge.current_equity
        
        # Max Drawdown Check
        if drawdown > challenge.max_drawdown:
            challenge.status = 'FAILED'
            return

        # Profit Target Check
        profit = challenge.current_equity - challenge.initial_balance
        if profit >= challenge.profit_target:
            challenge.status = 'PASSED'
            return
            
        # Daily Loss (Simplified: assuming we track daily PnL elsewhere or just check against fixed limit)
        # In a real app, we need to sum trades for today.
        pass

    @staticmethod
    def create_challenge(user, plan_type, settings):
        # Logic to create challenge based on plan settings
        initial_balance = 10000.0
        if plan_type == 'PRO': initial_balance = 50000.0
        if plan_type == 'ELITE': initial_balance = 100000.0
        
        challenge = UserChallenge(
            tenant_id=user.tenant_id,
            user_id=user.id,
            challenge_type=plan_type,
            initial_balance=initial_balance,
            current_equity=initial_balance,
            daily_max_loss=initial_balance * 0.05, # 5%
            max_drawdown=initial_balance * 0.10,   # 10%
            profit_target=initial_balance * 0.10,  # 10%
            status='ACTIVE'
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge
