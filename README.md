# RewardTrade - Powering the Future of Reward Points Exchange

---

## Overview

**RewardTrade** is a next-generation platform that transforms loyalty points into liquid assets. No more wasted reward points—our system enables users to trade, exchange, and invest their points effortlessly.

By integrating **Liquidity Pools** (for instant exchanges) and **Peer-to-Peer (P2P) Trading** (for market-driven exchanges), RewardTrade enhances user flexibility and merchant engagement.

### Key Benefits

- **For Users**: Flexibility to trade or instantly exchange reward points.
- **For Merchants**: Increased customer engagement and reduced liability on unclaimed points.
- **For the Ecosystem**: A balanced, transparent marketplace where loyalty points can be traded like real assets.

---

## Core Features

### Seamless User Experience

- Frictionless registration and authentication.
- Secure and intuitive user interface.

### Personalized User Profiles

Users can:

- Manage personal details.
- Link multiple reward accounts.
- Choose preferred trading currencies.
- Verify identity for secure transactions.

### Dynamic Reward Management

Our intelligent system tracks and optimizes reward balances across multiple merchants. Users can:

1. **Trade** points with others at dynamic rates.
2. **Exchange** points instantly from Liquidity pools.

### Instant & Secure Transactions

- **Real-time trade ledger** ensures fast processing.
- **Smart normalization engine** guarantees fair reward point valuation.

### Powerful Merchant API Integration

- Seamless API integration for merchants.
- Flexible redemption options to boost customer loyalty.

### Scalability & Security at the Core

RewardTrade is built using a modern, high-performance stack:

- **Flask** for backend services.
- **SQLAlchemy** for database management.
- **Celery & Redis** for high-speed processing.
- **SSH-256 encryption & MFA** for top-tier security.

---

## Technical Architecture

### Hybrid Exchange System

RewardTrade employs a **hybrid trading model**:

#### 1. Liquidity Pool (Instant Exchange)

- **Fixed-rate conversions** for instant transactions.
- **2-3% fee** for seamless execution.
- **Reserves maintained** via merchant agreements and automated replenishment.

#### 2. P2P Trading (Market-Driven Exchange)

- **Trade points dynamically** at dynamicly updated rates.
- **Low fees** (0.5%-1%).
- **Order book-based system** ensures liquidity.

#### 3. Hybrid Smart Routing

- **Small transactions** execute via Liquidity Pool.
- **Larger transactions** are hybrid (mixed Liquidity Pool + P2P) or full P2P.

### System Architecture

#### Core Components

- **User Interfaces**: Web and mobile apps.
- **Backend Services**:
  - Liquidity Pool Manager.
  - P2P Trading Engine.
  - Hybrid Routing System.
- **Database**:
  - User accounts & reward balances.
  - Merchant reserves & transactions.
  - P2P trade order book.
- **APIs**: Merchant integration.
- **Security Layer**: SSH-256 encryption, MFA.

#### Feature Implementation

- **Database**:
  - **SQLAlchemy-based** relational database for transactions & user data.

- **Security Measures**:
  - **Encryption**: SSH-256 for sensitive data.

---

## Business Model

### Revenue Streams

1. **Transaction Fees**:
   - **Instant exchanges**: 2-3%.
   - **Market trades**: 0.5%-1%.

2. **Merchant Subscriptions**:
   - **Basic** (Free).
   - **Premium** ($99/month).
   - **Enterprise** (Custom pricing).

3. **User Premium Features**:
   - **$4.99/month** for zero conversion fees & priority processing.

---

## Challenges & Solutions

### Emergency Protocols

- **System Crisis**: Pause transactions, secure balances, initiate recovery.
- **Market Crisis**: Circuit breakers, rate caps, liquidity reinforcements.

### Supporting Data & Case Studies

- **30%** of loyalty points remain unredeemed (Bond Brand Loyalty, 2022).
- **78%** of consumers prefer multi-merchant redemption (Deloitte, 2023).
- **P2P Market Efficiency**: Reduces transaction costs by **20-30%** (McKinsey, 2021).
- **Payback India Case Study**: **45% increase** in customer retention with an integrated system.
- **Security Advancements**: AI-driven fraud detection reduced losses by **40%** (IBM, 2023).
- **Scalability**: Cloud-based infrastructure ensures **99.99% uptime** (AWS Case Study).

---

## References

1. **Bond Brand Loyalty (2022)** – *Loyalty Report: Redemption Challenges and Trends.*
2. **Deloitte (2023)** – *Consumer Trends in Loyalty Programs.*
3. **McKinsey & Co. (2021)** – *The Role of P2P Systems in Modern Marketplaces.*
4. **Payback India (2022)** – *Annual Customer Retention Report.*
5. **IBM Security (2023)** – *AI and Fraud Detection in Digital Platforms.*

---

## Conclusion

**RewardTrade** is revolutionizing loyalty point utilization with its **hybrid exchange model, robust security, and intelligent routing system**. Whether you're a **user** maximizing reward points or a **merchant** boosting engagement, our platform offers the perfect ecosystem for limitless possibilities.

### Trade. Earn. Redeem.

The future of reward points starts here.


## Setup Instructions

1. Clone the repository:

git clone https://github.com/sashimss/NPCI_Ecell-Lunatics
cd rewardtrade


2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate


3. Install the required packages:

pip install -r requirements.txt


4. Set up the database:

 flask db init
 flask db migrate
 flask db upgrade


5. Start the Redis server (required for Celery):

  redis-server


6. In a new terminal, start the Celery worker:

celery -A app.celery worker --loglevel=info


7. In another terminal, start the Flask development server:

python run.py


8. Open a web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Features

- User registration and authentication
- View and manage loyalty points across multiple merchants
- Convert points between merchants using instant or smart exchange
- Automatic liquidity pool rebalancing

## API Endpoints

- `/api/<merchant>/rewards/<phone>`: Get user points for a specific merchant
- `/api/<merchant>/rewards/update`: Update user points for a specific merchant
- `/api/<merchant>/rewards/reset`: Reset user points for testing purposes
- `/api/health`: Check API status

## Known Issues and Future Improvements

- Implement proper error handling and logging
- Enhance security features (e.g., rate limiting, input validation)
- Improve calculation accuracy for point conversions
- Add unit tests and integration tests
- Implement a more sophisticated matching algorithm for smart exchanges

## Contributors

- Sashim Suryawanshi
- Akshay Harits
- Dhruv Goyal
- Ramuni Lalith Vishnu
