-- Database: `event_management`

-- Table structure for table `event`

CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `location` varchar(255) NOT NULL,
  `capacity` int(11) NOT NULL,
  `organizer` varchar(255) NOT NULL,
  `categories` varchar(255) NOT NULL,
  PRIMARY KEY (`event_id`)
) ;



-- Table structure for table `registration`


CREATE TABLE `registration` (
  `registration_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `attendee_name` varchar(255) DEFAULT NULL,
  `attendee_email` varchar(255) DEFAULT NULL,
  `attendee_phone` varchar(15) DEFAULT NULL,
  `registration_date` datetime NOT NULL,
  PRIMARY KEY (`registration_id`),
  KEY `event_id` (`event_id`)
)  ;


-- Table structure for table `ticket`


CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `Mail` varchar(100) NOT NULL,
  `price` float DEFAULT NULL,
  `quantity` varchar(10) NOT NULL,
  `ticket_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `event_id` (`event_id`)
)  ;




-- Table structure for table `users`


CREATE TABLE `users` (
  `Name` varchar(25) NOT NULL,
  `Dob` date NOT NULL,
  `Phone` varchar(10) NOT NULL,
  `Mail_ID` varchar(100) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `role` varchar(255) NOT NULL
) ;


