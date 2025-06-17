CREATE TABLE insurance_interest (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  age INT NOT NULL,
  gender VARCHAR(10),
  preferred_insurance_type VARCHAR(100),
  interest_level VARCHAR(50),
  submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
