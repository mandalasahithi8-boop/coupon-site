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
