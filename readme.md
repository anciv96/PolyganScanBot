## FAR Transaction Monitoring Telegram Bot
This project is a Telegram bot that monitors the movement of the Farcana (FAR) token in the Polygon blockchain and notifies users of transactions in a specific format. The bot is written in Python 3.12 using the aiogram 3 library and uses SQLite as the database. It is deployed in a Docker container.


### Table of Contents
* Description
* Features
* Technical Details
* Technologies Used
* Integration with Blockchain
* Security
* Admin Features
* Performance Requirements
* Installation Guide
* Prerequisites
* Installation Steps
* Usage
* Testing
* Future Expansion
* License
### Description
The FAR Transaction Monitoring Telegram Bot is designed to monitor all transactions involving the Farcana (FAR) token on the Polygon blockchain. The bot notifies the user about transactions involving specific wallets, which can be marked as "our wallets" or "unknown wallets". Notifications are sent in a specific format directly to a designated Telegram chat.

### Features
* __Transaction Monitoring__: Tracks all transactions of the FAR token in the Polygon network.
* __Wallet Identification__:
  * If a wallet is in the list of "our wallets", it displays its name or marks it as "Our wallet".
  * If a wallet is not in the list, it is displayed as "Unknown wallet" with its address.
* __Notification Format__:
  * Sends a message containing information about the wallet, transaction type, amount, balance change, and a direct link to the transaction on Polygonscan.
* __Real-time Alerts__: Sends notifications with minimal delay after a transaction is confirmed.
* __Admin Commands__:
  * `/update_wallets` — Update the list of monitored wallets.
  * `/status` — Check the status of the bot.
  * `/help` — Display available commands.
### Technical Details
#### Technologies Used
* __Programming Language__: Python 3.12
* __Libraries:__
  * aiogram 3 for Telegram bot interaction
  * SQLite for storing wallet information and balance data
* __APIs:__
  * Telegram Bot API for interacting with Telegram
  * Polygonscan API or WebSocket for real-time transaction monitoring
* __Deployment__: Docker container for 24/7 operation on a VPS server

#### Integration with Blockchain
* Uses the Polygonscan API to get transaction and balance information.
* Handles API rate limits and errors to ensure stable bot operation.
#### Security
* __API Token Protection__: API tokens and keys are securely stored using environment variables or configuration files outside the repository.
* __Error Handling__: Proper validation and exception handling are implemented to prevent bot failures.
### Admin Features
* __Update Wallet List__: The bot supports loading and updating the list of "our wallets" from an Excel or CSV file, keeping the association between wallet addresses and names.
* __Restricted Access__: Admin commands are only available to authorized users by Telegram ID.
### Performance Requirements
* __Notification Delay__: Maximum delay of 1 minute after a transaction occurs.
* __Scalability__: The bot can handle an increasing number of monitored wallets and transactions.
### Installation Guide
#### Prerequisites
* Python 3.12
* Docker
* API tokens for Telegram and Polygonscan
#### Installation Steps
1) **Clone the Repository:**:
  ```bash
  git clone <repository-url>
  cd <repository-folder>
  ```
2) **Set Up Environment Variables**: Create a `.env` file with your API tokens:
  ```env
  BOT_TOKEN=your_telegram_api_token
  POLYGON_KEY=your_polygonscan_api_token
  ```
3) 
**Build and Run with Docker:**
  ```
  docker build -t far-bot .
  docker run -d --name my-python-container far-bot
  ```

### Usage
Once the bot is up and running, it will automatically monitor transactions involving the FAR token on the Polygon blockchain. Authorized users can interact with the bot using the following commands:

* `/update_wallets`: Upload an updated list of "our wallets".
* `/status`: Check if the bot is running properly.
* `/help`: List all available commands.

### Testing
Testing includes:

* **Transaction Monitoring**: Ensuring the bot correctly identifies and monitors FAR transactions.
* **Message Formatting**: Verifying the correct format of messages sent to the user.
* **Error Handling**: Testing edge cases and unexpected scenarios to ensure stability.

### Future Expansion
The bot is designed with flexibility in mind, allowing for future functionality expansion, such as:

Adding new tokens for monitoring
Supporting multiple blockchains
Extending notification features to multiple channels