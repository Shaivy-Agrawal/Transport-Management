--admin_user
insert into admin_user(user_name, dob, address) values 
('souris', '1980-06-03', 'Doyens township'),
('shaivy', '2000-01-19', 'Hill Ridge'),
('ayush', '1992-11-18', 'Aparna Sarovar');

--administration
insert into administration(passcode, user_id) values 
('Google100', 12),
('helloworld', 11),
('transport4', 13);

--travel_agency
insert into travel_agency(agency_name, admin_id) values
('Sun Fortune', 14),
('Orange Travels', 13),
('Kaveri Travels', 15);

--agency_contact
insert into agency_contact values 
('4589357609', 3),
('7666392009', 4),
('9999000045', 4),
('2893888485', 5);

--bus_info
insert into bus_info values
('UP45GH7950', 'Secundrabad', 'Hyderabad', '2020-10-31 12:45:34', 23, 3, '2020-10-31'),
('PJ56JK3456', 'Delhi', 'mumbai', '2020-11-03 10:23:56', 34, 4, '2020-11-03'),
('TS89AK0026', 'Goa', 'Ooty', '2020-12-01 11:00:00', 70, 5, '2020-12-01');

--train_info
insert into train_info values
('TN88AS5433', 'Rajdhani', 'lucknow', '2020-11-10 12:45:34', 56, 'meerut', 4, '2020-11-10'),
('MP00DF1222', 'sharda', 'Mizoram', '2020-10-26 23:00:00', 16, 'MP', 3, '2020-10-26'),
('HP75ST8884', 'Duronto Express', 'Shimla', '2020-10-31 12:06:20', 100, 'Dehradun', 5, '2020-10-31');

insert into bus_driver values
('Gopal', '8932344432', 'UP45GH7950'),
('Ramu', '3344099090', 'TS89AK0026'),
('Hari Krishna', '9000003434', 'PJ56JK3456');

insert into user_contact values
('2333093029', 11),
('5555557483', 12),
('1209384958', 13);