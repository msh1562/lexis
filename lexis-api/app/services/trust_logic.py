from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.trust import TrustVote, VoteType
from ..models.block import Block
from ..models.user import User
from ..schemas.trust import TrustVoteCreate, TrustSummary


def create_vote(db: Session, vote_in: TrustVoteCreate) -> TrustVote:
    """Persist a user's trust vote."""
    if not db.query(Block).filter(Block.id == vote_in.block_id).first():
        raise ValueError("Invalid block id")
    if not db.query(User).filter(User.id == vote_in.user_id).first():
        raise ValueError("Invalid user id")

    vote = TrustVote(
        block_id=vote_in.block_id,
        user_id=vote_in.user_id,
        vote=vote_in.vote,
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote


def get_vote_summary(db: Session, block_id: int) -> TrustSummary:
    """Return count of trust and distrust votes for a block."""
    totals = (
        db.query(TrustVote.vote, func.count(TrustVote.id))
        .filter(TrustVote.block_id == block_id)
        .group_by(TrustVote.vote)
        .all()
    )
    trust = 0
    distrust = 0
    for vote_type, count in totals:
        if vote_type == VoteType.trust:
            trust = count
        else:
            distrust = count
    return TrustSummary(block_id=block_id, trust=trust, distrust=distrust)