# The original 44 hardcoded coupons - used by coupon_app/seed.py to
# populate the database on first run. The live site reads from the DB.
SEED_COUPONS = [
    # Food & Restaurants
    {"id": 1, "store": "Walmart", "title": "$5 off Groceries", "code": "GROCERY5", "category": "Food", "discount": "$5", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.walmart.com", "logo": "🛒"},
    {"id": 2, "store": "Uber Eats", "title": "Free delivery first order", "code": "FREEEAT", "category": "Food", "discount": "Free delivery", "expires": "Dec 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.ubereats.com", "logo": "🚗"},
    {"id": 3, "store": "Starbucks", "title": "Buy 1 Get 1 Free drinks", "code": "BOGO2024", "category": "Food", "discount": "BOGO", "expires": "Jun 30, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.starbucks.com", "logo": "☕"},
    {"id": 4, "store": "DoorDash", "title": "$0 delivery fee first order", "code": "DASH0FEE", "category": "Food", "discount": "Free delivery", "expires": "Aug 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.doordash.com", "logo": "🍔"},
    {"id": 5, "store": "McDonald's", "title": "Free fries with any order", "code": "MCDFRIES", "category": "Food", "discount": "Free fries", "expires": "Jul 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.mcdonalds.com", "logo": "🍟"},
    {"id": 6, "store": "Subway", "title": "Buy 1 footlong get 1 50% off", "code": "SUB50", "category": "Food", "discount": "50% off", "expires": "Sep 1, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.subway.com", "logo": "🥖"},
    {"id": 7, "store": "Pizza Hut", "title": "50% off all pizzas", "code": "PIZZA50", "category": "Food", "discount": "50%", "expires": "Jul 20, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.pizzahut.com", "logo": "🍕"},
    {"id": 8, "store": "Chipotle", "title": "Free chips & guac", "code": "CHIPGUAC", "category": "Food", "discount": "Free chips", "expires": "Aug 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.chipotle.com", "logo": "🌯"},

    # Hair & Beauty
    {"id": 9, "store": "Great Clips", "title": "$5 off any haircut", "code": "GC5OFF", "category": "Hair & Beauty", "discount": "$5", "expires": "Jul 31, 2025", "states": ["TX", "CA", "FL", "NY", "IL"], "cities": ["Dallas", "Houston", "Austin", "Los Angeles", "Miami", "Chicago", "New York"], "url": "https://www.greatclips.com", "logo": "✂️"},
    {"id": 10, "store": "Great Clips", "title": "Haircut for $8.99", "code": "GC899", "category": "Hair & Beauty", "discount": "$8.99", "expires": "Jun 30, 2025", "states": ["TX", "CA", "FL"], "cities": ["Dallas", "Fort Worth", "San Antonio", "Los Angeles", "Miami"], "url": "https://www.greatclips.com", "logo": "✂️"},
    {"id": 11, "store": "Supercuts", "title": "$2 off any service", "code": "SCUT2", "category": "Hair & Beauty", "discount": "$2", "expires": "Aug 1, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.supercuts.com", "logo": "💇"},
    {"id": 12, "store": "Sport Clips", "title": "Free MVP upgrade", "code": "SCMVP", "category": "Hair & Beauty", "discount": "Free upgrade", "expires": "Sep 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.sportclips.com", "logo": "🏆"},
    {"id": 13, "store": "Ulta Beauty", "title": "20% off entire purchase", "code": "ULTA20", "category": "Hair & Beauty", "discount": "20%", "expires": "Jul 4, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.ulta.com", "logo": "💄"},
    {"id": 14, "store": "Sally Beauty", "title": "Buy 2 get 1 free", "code": "SALLY3", "category": "Hair & Beauty", "discount": "BOGO", "expires": "Aug 20, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.sallybeauty.com", "logo": "💅"},
    {"id": 15, "store": "Sephora", "title": "Free shipping on $35+", "code": "SEPSHIP", "category": "Hair & Beauty", "discount": "Free shipping", "expires": "Dec 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.sephora.com", "logo": "🌸"},

    # Shopping
    {"id": 16, "store": "Amazon", "title": "10% off Electronics", "code": "ELEC10", "category": "Shopping", "discount": "10%", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.amazon.com", "logo": "📦"},
    {"id": 17, "store": "Target", "title": "$10 off $50 purchase", "code": "TARGET10", "category": "Shopping", "discount": "$10", "expires": "Aug 10, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.target.com", "logo": "🎯"},
    {"id": 18, "store": "Kohl's", "title": "30% off entire order", "code": "KOHLS30", "category": "Shopping", "discount": "30%", "expires": "Jul 25, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.kohls.com", "logo": "🛍️"},
    {"id": 19, "store": "Macy's", "title": "25% off clothing", "code": "MACY25", "category": "Shopping", "discount": "25%", "expires": "Aug 5, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.macys.com", "logo": "⭐"},
    {"id": 20, "store": "TJ Maxx", "title": "Extra 20% off clearance", "code": "TJM20", "category": "Shopping", "discount": "20%", "expires": "Sep 1, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.tjmaxx.com", "logo": "🏷️"},

    # Fashion
    {"id": 21, "store": "Nike", "title": "20% off shoes", "code": "SHOES20", "category": "Fashion", "discount": "20%", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.nike.com", "logo": "👟"},
    {"id": 22, "store": "H&M", "title": "25% off entire purchase", "code": "HM25OFF", "category": "Fashion", "discount": "25%", "expires": "Aug 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.hm.com", "logo": "👗"},
    {"id": 23, "store": "Gap", "title": "40% off full price styles", "code": "GAP40", "category": "Fashion", "discount": "40%", "expires": "Jul 20, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.gap.com", "logo": "👕"},
    {"id": 24, "store": "Old Navy", "title": "50% off everything", "code": "ON50ALL", "category": "Fashion", "discount": "50%", "expires": "Jun 30, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.oldnavy.com", "logo": "🧥"},
    {"id": 25, "store": "Adidas", "title": "30% off sitewide", "code": "ADI30", "category": "Fashion", "discount": "30%", "expires": "Aug 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.adidas.com", "logo": "⚽"},

    # Electronics
    {"id": 26, "store": "Best Buy", "title": "15% off laptops", "code": "LAPTOP15", "category": "Electronics", "discount": "15%", "expires": "Jul 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.bestbuy.com", "logo": "💻"},
    {"id": 27, "store": "Samsung", "title": "$100 off Galaxy phones", "code": "SAM100", "category": "Electronics", "discount": "$100", "expires": "Aug 1, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.samsung.com", "logo": "📱"},

    # Travel
    {"id": 28, "store": "Expedia", "title": "$50 off flights", "code": "FLY50", "category": "Travel", "discount": "$50", "expires": "Dec 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.expedia.com", "logo": "✈️"},
    {"id": 29, "store": "Airbnb", "title": "$40 off first stay", "code": "AIR40", "category": "Travel", "discount": "$40", "expires": "Sep 30, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.airbnb.com", "logo": "🏠"},
    {"id": 30, "store": "Enterprise", "title": "25% off car rental", "code": "ENT25", "category": "Travel", "discount": "25%", "expires": "Aug 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.enterprise.com", "logo": "🚗"},

    # Health
    {"id": 31, "store": "CVS", "title": "40% off vitamins", "code": "CVSVIT40", "category": "Health", "discount": "40%", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.cvs.com", "logo": "💊"},
    {"id": 32, "store": "Walgreens", "title": "$5 off $25 purchase", "code": "WAG5OFF", "category": "Health", "discount": "$5", "expires": "Aug 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.walgreens.com", "logo": "🏥"},
    {"id": 33, "store": "Planet Fitness", "title": "$0 enrollment fee", "code": "PFIT0", "category": "Health", "discount": "Free enrollment", "expires": "Sep 1, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.planetfitness.com", "logo": "💪"},

    # Pets
    {"id": 34, "store": "Chewy", "title": "30% off pet supplies", "code": "PET30", "category": "Pets", "discount": "30%", "expires": "Aug 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.chewy.com", "logo": "🐾"},
    {"id": 35, "store": "PetSmart", "title": "$10 off $50 purchase", "code": "PSMART10", "category": "Pets", "discount": "$10", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.petsmart.com", "logo": "🐶"},

    # Home
    {"id": 36, "store": "Home Depot", "title": "10% off tools", "code": "HDTOOL10", "category": "Home", "discount": "10%", "expires": "Aug 4, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.homedepot.com", "logo": "🔨"},
    {"id": 37, "store": "IKEA", "title": "$25 off $150 purchase", "code": "IKEA25", "category": "Home", "discount": "$25", "expires": "Sep 15, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.ikea.com", "logo": "🛋️"},
    {"id": 38, "store": "Lowe's", "title": "10% off appliances", "code": "LOWAPP10", "category": "Home", "discount": "10%", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.lowes.com", "logo": "🏡"},

    # Entertainment
    {"id": 39, "store": "Netflix", "title": "First month free", "code": "NETFREE", "category": "Entertainment", "discount": "Free month", "expires": "Dec 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.netflix.com", "logo": "🎬"},
    {"id": 40, "store": "Spotify", "title": "3 months for $0.99", "code": "SPOT99", "category": "Entertainment", "discount": "$0.99", "expires": "Aug 1, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.spotify.com", "logo": "🎵"},
    {"id": 41, "store": "AMC Theaters", "title": "$5 Tuesday tickets", "code": "AMCTUE5", "category": "Entertainment", "discount": "$5", "expires": "Dec 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.amctheatres.com", "logo": "🎥"},

    # Auto
    {"id": 42, "store": "Jiffy Lube", "title": "$10 off oil change", "code": "JLUBE10", "category": "Auto", "discount": "$10", "expires": "Sep 30, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.jiffylube.com", "logo": "🔧"},
    {"id": 43, "store": "AutoZone", "title": "20% off any order", "code": "AZ20OFF", "category": "Auto", "discount": "20%", "expires": "Aug 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.autozone.com", "logo": "🚙"},
    {"id": 44, "store": "Firestone", "title": "$20 off tire rotation", "code": "FIRE20", "category": "Auto", "discount": "$20", "expires": "Jul 31, 2025", "states": ["All"], "cities": ["All"], "url": "https://www.firestonecompleteautocare.com", "logo": "🛞"},
]

states_list = ["All States", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
               "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
               "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
               "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# NOTE: the original file had two "TX" keys, so the second silently
# overwrote the first and dropped Arlington/Plano/Lubbock. Merged here.
cities_by_state = {
    "TX": ["All Cities", "Dallas", "Houston", "Austin", "San Antonio", "Fort Worth", "El Paso", "Arlington", "Plano", "Lubbock"],
    "CA": ["All Cities", "Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose", "Fresno", "Oakland"],
    "FL": ["All Cities", "Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale", "Tallahassee", "Naples"],
    "NY": ["All Cities", "New York City", "Buffalo", "Albany", "Rochester", "Syracuse", "Yonkers"],
    "IL": ["All Cities", "Chicago", "Aurora", "Naperville", "Rockford", "Springfield", "Joliet"],
    "GA": ["All Cities", "Atlanta", "Augusta", "Columbus", "Savannah", "Athens"],
    "WA": ["All Cities", "Seattle", "Spokane", "Tacoma", "Bellevue", "Everett"],
}
