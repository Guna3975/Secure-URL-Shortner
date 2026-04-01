from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from app.database.connection import get_db
from app.database.redis_connection import get_redis
import secrets
import string

router = APIRouter(prefix="/url", tags=["url"])

class ShortenRequest(BaseModel):
    long_url: str
    custom_alias: str | None = Field(default=None, min_length=1, max_length=20)


# ====================== SHORTEN with Strong Deduplication ======================
@router.post("/shorten")
def shorten_url(request: ShortenRequest, db=Depends(get_db), redis=Depends(get_redis)):
    cursor = db.cursor()
    
    # Normalize URL
    long_url = request.long_url.strip()
    normalized_url = long_url.rstrip('/').lower()
    
    # Check for existing URL
    cursor.execute("""
        SELECT short_code
        FROM short_urls
        WHERE original_url = :1
           OR original_url = :2
           OR TRIM(original_url) = TRIM(:3)
           OR LOWER(TRIM(original_url)) = :4
    """, [long_url, long_url.rstrip('/'), long_url, normalized_url])
    
    existing = cursor.fetchone()
    if existing:
        short_code = existing[0]
        short_url = f"http://localhost:8000/url/{short_code}"
        
        if redis:
            redis.set(short_code, long_url, ex=86400)
        
        return {
            "short_url": short_url,
            "message": "Existing short URL returned (duplicate prevented)"
        }

    # Create new short code
    if request.custom_alias:
        short_code = request.custom_alias.strip()
    else:
        short_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

    try:
        cursor.execute("""
            INSERT INTO short_urls (short_code, original_url, created_at)
            VALUES (:1, :2, CURRENT_TIMESTAMP)
        """, [short_code, long_url])
        
        db.commit()

        if redis:
            redis.set(short_code, long_url, ex=86400)
            # === Redis Limit: Keep only last 10 short codes ===
            redis.lpush("recent_short_codes", short_code)
            redis.ltrim("recent_short_codes", 0, 9)

        return {
            "short_url": f"http://localhost:8000/url/{short_code}",
            "message": "New short URL created successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to shorten: {str(e)}")


# ====================== MY LINKS ======================
@router.get("/my-links")
def get_my_links(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT short_code, original_url, created_at, click_count
        FROM short_urls
        ORDER BY created_at DESC
        FETCH FIRST 10 ROWS ONLY
    """)
    rows = cursor.fetchall()
    
    links = [{
        "short_code": row[0],
        "short_url": f"http://localhost:8000/url/{row[0]}",
        "original_url": row[1],
        "created_at": str(row[2]),
        "click_count": row[3] or 0
    } for row in rows]
    
    return {"links": links}


# ====================== ANALYTICS ======================
@router.get("/analytics")
def get_analytics(db=Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM short_urls")
    total_links = cursor.fetchone()[0]

    cursor.execute("SELECT NVL(SUM(click_count), 0) FROM short_urls")
    total_clicks = cursor.fetchone()[0]

    avg = round(total_clicks / total_links, 1) if total_links > 0 else 0

    cursor.execute("""
        SELECT short_code, original_url, click_count
        FROM short_urls
        ORDER BY click_count DESC
        FETCH FIRST 3 ROWS ONLY
    """)
    top = cursor.fetchall()
    
    top_links = [{
        "short_code": r[0],
        "short_url": f"http://localhost:8000/url/{r[0]}",
        "original_url": r[1],
        "click_count": r[2] or 0
    } for r in top]

    return {
        "total_links": total_links,
        "total_clicks": total_clicks,
        "avg_clicks_per_link": avg,
        "top_links": top_links
    }


# ====================== REDIRECT with Redis Limit (10 only) ======================
@router.get("/{short_code}")
async def redirect_url(short_code: str, redis=Depends(get_redis), db=Depends(get_db)):
    if short_code in ["shorten", "my-links", "analytics"]:
        raise HTTPException(status_code=404, detail="Not found")

    long_url = None

    # Try Redis first
    if redis:
        long_url = redis.get(short_code)

    # If not in Redis → Look in Database
    if not long_url:
        cursor = db.cursor()
        cursor.execute("SELECT original_url FROM short_urls WHERE short_code = :1", [short_code])
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Short URL not found")
        
        long_url = row[0]
        
        # Cache back to Redis and maintain limit of 10
        if redis:
            redis.set(short_code, long_url, ex=86400)
            redis.lpush("recent_short_codes", short_code)
            redis.ltrim("recent_short_codes", 0, 9)   # Keep only last 10

    # === 10 Click Limit ===
    cursor = db.cursor()
    cursor.execute("SELECT click_count FROM short_urls WHERE short_code = :1", [short_code])
    click_count = cursor.fetchone()[0] or 0

    if click_count >= 10:
        cursor.execute("DELETE FROM short_urls WHERE short_code = :1", [short_code])
        db.commit()
        if redis:
            redis.delete(short_code)
        raise HTTPException(status_code=410, detail="This link has expired after reaching 10 clicks.")

    # Increment click count
    try:
        cursor.execute("""
            UPDATE short_urls
            SET click_count = click_count + 1
            WHERE short_code = :1
        """, [short_code])
        db.commit()
    except:
        pass

    return RedirectResponse(url=long_url)