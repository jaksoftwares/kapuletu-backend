class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True)
    action = Column(String)
    entity_type = Column(String)