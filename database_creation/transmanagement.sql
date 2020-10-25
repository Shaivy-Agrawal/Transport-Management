create table customer(
adhaar_no		varchar(12)  primary key,
c_name			varchar(30)  not null,
dob				date		 not null,
check(adhaar_no ~ '[0-9]{12}')
);

create table payment(
payment_id		serial       primary key,
amount			money		 not null,
p_date			date		 not null,
adhaar_no		varchar(12)	 unique not null,
res_id			integer		 not null,
foreign key (adhaar_no) references customer(adhaar_no),
foreign key(res_id) references reservation(res_id)
);

create table reservation(
res_id		 	serial       primary key,
start_date		date 		 not null,
travel_mode		varchar(6)   not null,
vehicle_no		varchar(10)	 not null,
adhaar_no		varchar(12)	 not null,
destination		varchar(30)	 not null,
agency_id		integer		 not null,
seat_no			integer		 not null,
foreign key (adhaar_no) references customer(adhaar_no),
foreign key (payment_id) references payment(payment_id),
foreign key (agency_id) references travel_agency(agency_id),
check(travel_mode in ('Bus', 'Train'))
);

create table address(
house_no 		integer		 not null,
locality		varchar(30)  not null,
city			varchar(20)	 not null,
c_state			varchar(20)  not null,
pin_code		integer		 not null,
adhaar_no		varchar(12)	 unique not null,
foreign key (adhaar_no) references customer(adhaar_no)
);

create table customer_contact(
contact_no		varchar(10)	 primary key,
adhaar_no		varchar(12)  not null,
foreign key (adhaar_no) references customer(adhaar_no),
check(contact_no ~ '[1-9]{1}[0-9]{9}')
);

create table admin_user(
user_id			serial       primary key,
user_name		varchar(20)  not null,
dob				date		 not null,
address			varchar(150) not null
);

create table user_contact(
contact_no		varchar(10)	 primary key,
user_id			integer		 not null,
foreign key (user_id) references admin_user(user_id)
);

create table administration(
admin_id		serial       primary key,
passcode 		varchar(30)	 not null,
user_id			integer		 unique not null,
foreign key (user_id) references admin_user(user_id)
);

create table travel_agency(
agency_id		serial       primary key,
agency_name		varchar(30)	 not null,
admin_id		integer		 not null,
foreign key (admin_id) references administration(admin_id)
);

create table agency_contact(
contact_no		varchar(10)	 primary key,
agency_id		integer		 not null,
foreign key (agency_id) references travel_agency(agency_id),
check(contact_no ~ '[1-9]{1}[0-9]{9}')
);

create table booking_reciept(
booking_id		serial       primary key,
b_status     	varchar(10)  not null,
b_date			date		 not null,
travel_mode		varchar(6)	 not null,
destination		varchar(100) not null,
vehicle_no		varchar(10)  not null,
seat_no 		integer		 not null,
admin_id		integer  	 not null,
adhaar_no		varchar(12)	 not null,
res_id		 	integer		 not null,
foreign key (admin_id) references administration(admin_id),
foreign key (adhaar_no) references customer(adhaar_no),
foreign key(res_id) references reservation(res_id),
check(b_status in ('Waiting', 'Confirmed', 'Cancelled'))
);

create table train_info(
train_no 		varchar(10)	 primary key,
train_name		varchar(30)	 not null,
start_station	varchar(30)  not null,
depart_time     timestamp	 not null,
seats_left      integer      not null,
destination		varchar(50)  not null,
agency_id		integer		 not null,
depart_date		date		 not null,
foreign key (agency_id) references travel_agency(agency_id)
);

create table bus_info(
bus_no			varchar(10)  primary key,
start_station	varchar(30)	 not null,
destination		varchar(30)	 not null,
depart_time		timestamp	 not null,
seats_left		integer		 not null,
agency_id		integer		 not null,
depart_date 	date		 not null,
foreign key (agency_id) references travel_agency(agency_id)
);

create table bus_driver(
driver_name		varchar(30)  not null,
contact_no		varchar(10)  unique not null,
bus_no			varchar(10)  not null,
foreign key (bus_no) references bus_info(bus_no),
check(contact_no ~ '[1-9]{1}[0-9]{9}')
);	