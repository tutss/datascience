from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import pandas as pd

from constants import DELEGACIAS


delegacias = pd.Series(DELEGACIAS).rename("nome")          # {id: nome}
geolocator = Nominatim(user_agent="ssp-crawler")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

coords = (
    delegacias
    .apply(lambda n: n.replace('DP', 'Distrito Policial', 1))
    .apply(lambda n: geocode(f"{n}, São Paulo, SP, Brazil"))
    .apply(lambda loc: (loc.latitude, loc.longitude) if loc else (None, None))
    .apply(pd.Series)
    .rename(columns={0: "lat", 1: "lon"})
)

delegacias.to_frame().join(coords).reset_index().rename(columns={"index": "id"})\
          .to_csv("delegacias_coords.csv", index=False)