# Guitar Auctions

## Project Description

An eBay-like e-commerce auction site for guitars that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Features

### Key Features:

- **User Registration and Login**:
  - Users can register, log in, and log out.
  - User authentication is required to access various features.

- **Create Auction Listings**:
  - Users can create auction listings with a title, description, starting bid, optional image URL, and category.

- **Active Listings Page**:
  - Displays all active auction listings with essential details (title, description, current price, photo).

- **Listing Detail Page**:
  - Users can view detailed information about a listing, including the current bid.
  - Option to add the item to a **Watchlist** (or remove it if already added).
  - Users can place a bid (must be higher than the starting bid and any existing bids).
  - If the user created the listing, they can close the auction.

- **Watchlist**:
  - Signed-in users can view and manage their watchlist, which contains all listings they have saved.

- **Bid on Listings**:
  - Bidding is restricted to being higher than the current bid and starting bid.
  - Once the auction is closed, the highest bidder wins.

- **Comment on Listings**:
  - Users can comment on listings, and comments will be displayed on the listing page.

- **Listing Categories**:
  - Users can browse listings by category (e.g., Fashion, Electronics, Home).

- **User’s Own Listings**:
  - A **"My Listings"** button allows users to view and manage their own auction listings.

- **Django Admin Interface**:
  - Admins can view, add, edit, or delete listings, bids, and comments.

- **Auction Status**:
  - If the auction is closed, the page will display if the user has won the auction.


## Technologies Used

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Django, Python, SQLite

## Getting Started

### Prerequisites

Create a virtual environment

```bash
python3 -m venv venv
```
Activate the virtual environment:

- On macOS/Linux:

```bash
source venv/bin/activate
```

- On Windows:

```bash
venv\Scripts\activate
```

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SoroushKeyana/Guitar-Auctions.git
   ```
2. Go to Guitar-Auctions directory:
   ```bash
    cd Guitar-Auctions
   ```

4. Install the dependencies:


    ```bash
    pip install -r requirements.txt
    ```

5. Create .env file: Create a file named .env in the same directory and add the following line to it. Remember to add your secret key to it.

    ```bash
    SECRET_KEY='your-generated-secret-key-here'
    ```

6. Run database migrations:

    ```bash 
    python manage.py makemigrations auctions
    ```

    ```bash
    python manage.py migrate
    ```

## Running the Application
    
    python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser to see the application running locally.
