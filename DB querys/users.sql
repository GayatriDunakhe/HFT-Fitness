CREATE DATABASE hft_fitness;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL,
    pwd VARCHAR(128) NOT NULL
);

INSERT INTO users (email, pwd) VALUES ( 'gayatri@gmail.com', '12345');

CREATE TABLE activity (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    activity_type VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    intensity INT NOT NULL,
    calories_burned INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE users
ADD COLUMN age INT,
ADD COLUMN height DECIMAL(5, 2),
ADD COLUMN weight DECIMAL(5, 2),
ADD COLUMN gender ENUM('Male', 'Female', 'Other');

ALTER TABLE users
ADD COLUMN name VARCHAR(255);

CREATE TABLE sleep (
    sleep_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hours_slept DECIMAL(4, 2),
    sleepiness_level VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE mood (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mood_rating VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE sleep ADD COLUMN duration DECIMAL(5, 2);

CREATE TABLE category (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    categoryName VARCHAR(255) NOT NULL
);

CREATE TABLE food (
    foodID INT PRIMARY KEY AUTO_INCREMENT,
    foodName VARCHAR(255) NOT NULL,
    categoryID INT,
    calories INT,
    carbohydrates INT,
    proteins INT,
    fats INT,
    descr TEXT,
    imageURL VARCHAR(255),
    FOREIGN KEY (categoryID) REFERENCES category(categoryID)
);

INSERT INTO category (categoryName)
VALUES
    ('Breakfast'),
    ('Lunch'),
    ('Dinner');

INSERT INTO food (foodName, categoryID, calories, carbohydrates, proteins, fats, descr, imageURL)
VALUES
    ('Chapathi', 3, 60, 20, 15, 25, 'Chapathi is a type of Indian bread made from wheat flour.', 'https://th.bing.com/th/id/OIP.UVycUOJ7YqHdUngWP68ovQHaHP?pid=ImgDet&w=679&h=664&rs=1'),
    ('Pulkha', 3, 50, 20, 20, 10, 'Pulkha is similar to Chapathi, made from wheat flour.', 'https://3.bp.blogspot.com/_91gg-nFfS3E/S89pHCNdqWI/AAAAAAAAATM/GB2SupEoJUg/s1600/DSC01046.JPG'),
    ('Vegetable Salad', 3, 100, 40, 40, 20, 'A healthy salad made with fresh vegetables.', 'https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?cs=srgb&dl=vegetable-salad-on-plate-1059905.jpg&fm=jpg'),
    ('Fruit Salad', 3, 120, 50, 60, 40, 'A delicious mix of fresh fruits.', 'https://www.momontimeout.com/wp-content/uploads/2021/06/fruit-salad-square.jpeg');

INSERT INTO food (foodName, categoryID, calories, carbohydrates, proteins, fats, descr, imageURL)
VALUES
    ('Basmati Rice', 2, 176, 50, 8, 2, '50g Basmati Rice contains 176 cal.','https://indiaphile.info/wp-content/uploads/2013/05/basmatirice-2.jpg'),
    ('Chicken Curry', 2, 101, 32, 30, 40, 'One Bowl Chicken curry gives 101 calories.', 'https://th.bing.com/th/id/OIP.nTT5tvHk0Up59zRcC6oEygHaHa?pid=ImgDet&rs=1'),
    ('Butter Naan', 2, 65, 40, 8, 18, 'One naan contains 65 Calories.', 'https://i.pinimg.com/originals/2c/df/63/2cdf631f081844644ca9e65bc3d22c58.jpg'),
    ('Dal', 2, 230, 60, 15, 3, '100g Dal contains 230 cal.', 'https://i0.wp.com/vegecravings.com/wp-content/uploads/2018/01/Dal-Tadka-Recipe-Step-By-Step-Instructions.jpg?fit=2421%2C1944&quality=30&strip=all&ssl=1');

INSERT INTO food (foodName, categoryID, calories, carbohydrates, proteins, fats, descr, imageURL)
VALUES
    ('Idly', 1, 58, 52, 8, 21, 'One Idly gives 58 calories.', 'https://www.kindpng.com/picc/m/333-3335906_idli-in-white-background-hd-png-download.png'),
    ('Dosa', 1, 133, 75, 11, 47, 'One Dosa gives 133 calories.', 'https://wallpapercave.com/wp/wp6734919.jpg'),
    ('Puri', 1, 101, 30, 5, 67, 'One Puri gives 101 calories.', 'https://www.seekpng.com/png/detail/254-2548049_poori-puri-indian-food-png-hd-stock-photos.png'),
    ('Bonda', 1, 68, 25, 10, 33, 'One Bonda gives 68 calories.', 'https://th.bing.com/th?id=OIP.i6WH8mNfTuY0VoV2T7NYigHaFj&w=288&h=216&c=8&rs=1&qlt=90&o=6&dpr=1.5&pid=3.1&rm=2');

CREATE TABLE diet_plan (
	diet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_name VARCHAR(255) NOT NULL,
    calories INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
