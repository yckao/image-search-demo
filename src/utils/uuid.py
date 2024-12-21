from datetime import datetime
import uuid
from typing import Optional

def uuid7(timestamp: Optional[datetime] = None) -> uuid.UUID:
    """
    Generate a UUID v7 - A timestamp-based UUID that is sortable.
    
    Args:
        timestamp (datetime, optional): Timestamp to use for generation. 
            Defaults to current time if None.
    
    Returns:
        uuid.UUID: A new UUID v7 instance
    
    Reference:
        https://www.ietf.org/archive/id/draft-peabody-dispatch-new-uuid-format-04.html#name-uuid-version-7
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    # Convert timestamp to milliseconds since Unix epoch
    milliseconds = int(timestamp.timestamp() * 1000)
    
    # Create a 48-bit timestamp value (UUID v7 spec)
    timestamp_hex = format(milliseconds, '012x')
    
    # Generate random bits for the remaining bytes
    random_bytes = uuid.uuid4().bytes[6:]
    
    # Combine timestamp hex with random data and set version/variant bits
    uuid_hex = (
        timestamp_hex +                # 48 bits for timestamp
        '7' +                         # Version 7
        format(random_bytes[0] & 0x0F, 'x') +  # Clear first 4 bits
        bytes.hex(random_bytes[1:])   # Remaining random bytes
    )
    
    return uuid.UUID(uuid_hex)