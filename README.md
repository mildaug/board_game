# Board Game Hub

Welcome to Board Game Hub! This is a web application designed to be your one-stop destination for all things related to adventurous, fun, and geeky board games. Whether you are a seasoned gamer or just starting your board game journey, Board Game Hub has got you covered.


## Features

- **Browse Games:** Explore a vast collection of board games from various genres, including adventure, strategy, fantasy, and more. Get detailed information about each game, such as its publisher, year of release, player count, duration, and recommended age.

- **Game Details:** Dive deep into the world of your favorite games. View high-quality images, watch game trailers, read user reviews and ratings, and leave your own feedback.

- **Borrow and Lend Games:** Connect with other board game enthusiasts and borrow or lend games. Easily submit borrowing requests, track borrowed games, and mark games as returned.

- **User Ratings and Reviews:** Share your thoughts and experiences by rating and reviewing games. Read reviews from other users to get insights and recommendations.

- **Search and Filters:** Find games quickly with our powerful search functionality. Apply filters based on categories, difficulty level, player count, and more to discover games that match your preferences.


## Installation

To run Board Game Hub on your local machine, please make sure you have the following dependencies installed:

- asgiref==3.7.2
- Django==4.2.2
- Pillow==9.5.0
- sqlparse==0.4.4
- typing_extensions==4.6.3

Follow these steps to get started:

1. Clone the repository from GitHub:
git clone https://github.com/your-username/board-game-hub.git

2. Navigate to the project directory:
cd board-game-hub

3. Create a virtual environment:
python3 -m venv venv

4. Activate the virtual environment:

- For Windows:

  ```
  venv\Scripts\activate
  ```

- For macOS and Linux:

  ```
  source venv/bin/activate
  ```

5. Install the required dependencies:
pip install -r requirements.txt

6. Run database migrations:
python manage.py migrate

7. Start the development server:
python manage.py runserver

8. Access Board Game Hub in your web browser at `http://localhost:8000`.


## Contributing

We welcome contributions to Board Game Hub! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue on our GitHub repository.

To contribute code changes, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push the changes to your forked repository.
5. Open a pull request, describing your changes in detail.

Happy gaming!