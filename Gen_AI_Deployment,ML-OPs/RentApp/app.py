rent_listings = [
    {"name": "Green View Apartment", "city": "Bengaluru", "monthly_rent": 18000},
    {"name": "Lake Side Studio", "city": "Pune", "monthly_rent": 15000},
    {"name": "Metro Homes", "city": "Hyderabad", "monthly_rent": 22000},
]


def show_listings():
    print("Available RentApp Listings")
    print("-" * 30)
    for index, listing in enumerate(rent_listings, start=1):
        print(f"{index}. {listing['name']} - {listing['city']} - Rs. {listing['monthly_rent']}/month")


def calculate_total_monthly_rent():
    return sum(listing["monthly_rent"] for listing in rent_listings)


if __name__ == "__main__":
    show_listings()
    print("-" * 30)
    print(f"Total monthly rent of all listings: Rs. {calculate_total_monthly_rent()}")
