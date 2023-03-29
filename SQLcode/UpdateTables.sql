show global variables like 'local_infile';
set global local_infile=true;

create table dash.saledata (
OrderID	varchar(10) DEFAULT NULL,
OrderDate	Date DEFAULT NULL,
Gender	varchar(10) DEFAULT NULL,
AgeGroup	varchar(10) DEFAULT NULL,
Channel	varchar(10) DEFAULT NULL,
ShipDate	Date DEFAULT NULL,
ItemCode	varchar(10) DEFAULT NULL,
MapCode	varchar(10) DEFAULT NULL,
Quantity	int DEFAULT NULL,
Revenue	int DEFAULT NULL,
Cost	int DEFAULT NULL,
Category	varchar(10) DEFAULT NULL,
Item Type	varchar(10) DEFAULT NULL,
Region	varchar(10) DEFAULT NULL,
Country	varchar(10) DEFAULT NULL,
Code2	varchar(10) DEFAULT NULL,
Code3	varchar(10) DEFAULT NULL,
Latitude	float DEFAULT NULL,
Longitude	float DEFAULT NULL
);

load data local infile '/Users/minkyoung/Documents/Dev/DashBoard_basic/practice_data/Salesdata/Data.csv' 
into table dash.saledata
CHARACTER SET 'euckr'
FIELDS 
	TERMINATED BY ','
	IGNORE 1 LINES;
    
    
