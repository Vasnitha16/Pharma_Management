use pharmacy_db;

CREATE TABLE IF NOT EXISTS user_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS pharmacy_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    pharmacy_id INT ,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)
);

CREATE TABLE IF NOT EXISTS pharmacies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,      
    description TEXT,                 
    price DECIMAL(10, 2),  
    quantity INT,
    supplier_id INT,                  
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ,
    pharmacy_id INT,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)    
);

CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pharmacy_id INT,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)
);

CREATE TABLE cart (
    user_id INT,
    medicine_id INT,
    quantity INT,
    PRIMARY KEY (user_id, medicine_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

CREATE TABLE bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medicine_id INT NOT NULL,
    pharmacy_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_credentials(id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(id),
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)
);



INSERT INTO medicines (name, pharmacy_id, price, quantity, description,supplier_id) VALUES
('Paracetamol', 1, 2.50, 100, 'Used to treat mild to moderate pain and fever',1),
('Ibuprofen', 1, 5.00, 50, 'Nonsteroidal anti-inflammatory drug for pain and inflammation',1),
('Amoxicillin', 2, 12.00, 200, 'Antibiotic used to treat bacterial infections',2),
('Cetirizine', 2, 3.00, 150, 'Antihistamine used to relieve allergy symptoms',2),
('Aspirin', 3, 4.00, 75, 'Used to reduce pain, fever, or inflammation',3);

INSERT INTO medicines (name, pharmacy_id, price, quantity, description, supplier_id) VALUES
('Metformin', 3, 8.00, 120, 'Medication used to manage type 2 diabetes', 3),
('Omeprazole', 1, 6.50, 80, 'Proton pump inhibitor used for acid reflux and ulcers', 1),
('Losartan', 2, 10.00, 60, 'Used to treat high blood pressure and protect kidneys', 2),
('Ciprofloxacin', 3, 15.00, 90, 'Antibiotic used to treat bacterial infections', 3),
('Levothyroxine', 1, 4.50, 100, 'Used to treat hypothyroidism by replacing thyroid hormone', 1),
('Simvastatin', 2, 7.00, 150, 'Used to lower cholesterol and reduce heart disease risk', 2),
('Clopidogrel', 3, 11.00, 110, 'Antiplatelet drug used to prevent strokes and heart attacks', 3),
('Salbutamol', 1, 3.50, 200, 'Bronchodilator used to treat asthma and breathing disorders', 1),
('Doxycycline', 2, 9.50, 85, 'Antibiotic used to treat infections and acne', 2),
('Ranitidine', 3, 5.00, 70, 'Histamine blocker used to treat and prevent ulcers', 3);



INSERT INTO suppliers (name, pharmacy_id) VALUES 
    ('HealthPlus Supplies', 1),
    ('MediTrust Pharmaceuticals', 2),
    ('PharmaCare', 3),
    ('Wellness Distributors', 1),
    ('PureMed', 2);

INSERT INTO pharmacies (name) VALUES ('CityCare Pharmacy');
INSERT INTO pharmacies (name) VALUES ('Wellness Pharmacy');
INSERT INTO pharmacies (name) VALUES ('HealthPlus Pharmacy');

DELIMITER //

CREATE TRIGGER prevent_duplicate_user_username
BEFORE INSERT ON user_credentials
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM user_credentials WHERE username = NEW.username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate username not allowed in user_credentials!';
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER prevent_duplicate_pharmacy_username
BEFORE INSERT ON pharmacy_credentials
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM pharmacy_credentials WHERE username = NEW.username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate username not allowed in pharmacy_credentials!';
    END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE InsertBill(
    IN p_user_id INT,
    IN p_medicine_id INT,
    IN p_pharmacy_id INT,
    IN p_quantity INT,
    IN p_total_price DECIMAL(10, 2)
)
BEGIN
    INSERT INTO bills (user_id, medicine_id, pharmacy_id, quantity, total_price)
    VALUES (p_user_id, p_medicine_id, p_pharmacy_id, p_quantity, p_total_price);
END //

DELIMITER ;


