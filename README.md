# 💸 MoneyMinder
MoneyMinder is 100% open-source python console-based application designed to help users manage their accounts by keeping track of balances, setting goals, tracking credits and debits, and providing a convenient way to view their current balance. 

## ⚠️ Important Note
This application is currently under development and serves as a valuable learning experience for python programming.

## Prerequisites

Make sure you have met the following prerequisites

- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/cli/pip_download/)
- [VSCodium](https://github.com/VSCodium/vscodium/releases), [PyCharm](https://www.jetbrains.com/pycharm/) or any IDE.
- [MySQL](https://www.mysql.com/downloads/)
- [Adminer](https://www.adminer.org/), [PhpMyAdmin](https://www.phpmyadmin.net/downloads/) or any database management GUI if needed.

### Using Docker

If you prefer not to set up a MySQL database manually, I have provided a `docker-compose.yml` file at the root of the project. This file will set up a MySQL database and Adminer, a web-based database management tool, for you.

Make sure you have met the following prerequisites

- [Docker](https://www.docker.com/get-started) 
- [Docker Compose](https://docs.docker.com/compose/install/) 


1. Run the following command to start the services
    ```bash
    docker-compose up
    ```

2. Create a `.env` file based on `.env.example`

3. Update **MYSQL_** rows that are used with `docker-compose.yml`
    ```bash
    MYSQL_ROOT_PASSWORD=your_mysql_root_password
    MYSQL_DATABASE=your_mysql_databse
    MYSQL_USER=your_mysql_username
    MYSQL_PASSWORD=your_mysql_user_password
    ```

4. Access the Adminer interface in your web browser by navigating to `http://localhost:8080`.

**WARNING:** Docker services use the port `3306` for MySQL and `8080` for Adminer. Ensure these ports are available on your machine before running the command.

## Get Started

1. Clone the repository
    ```bash
    https://github.com/asyncmagician/MoneyMinder.git
    ```

2. Install required dependancies with *pip*
    ```bash
    pip install -r requirements.txt
    ```

3. Update the `.env` file based on `.env.example`
    ```bash
    DB_HOST=your_host
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_DATABASE=your_database
    ```

4. Run the main file to start the application
    ```bash
    python3 main.py
    ```

## License
MoneyMinder is released under the Apache License 2.0. See `LICENSE` for more information.

The Apache License 2.0 is a permissive open source license that allows you, as the owner of the project, to grant others the right to use, modify, distribute, and even sell the software while still maintaining your ownership rights. By choosing the Apache License 2.0, you are allowing others to freely use and contribute to the project while giving them the freedom to build upon it and create derivative works.

To learn more about the Apache License 2.0, please visit http://www.apache.org/licenses/LICENSE-2.0.

## Contributing
I welcome contributions from the community. If you find any issues or have feature suggestions, feel free to open an issue or submit a pull request on GitHub. The 
only requirement is that you need to sign your commits.

## Contact
If you have any questions or inquiries about the project, feel free to reach out to me on [Twitter](https://twitter.com/asyncmaster) 🐦
