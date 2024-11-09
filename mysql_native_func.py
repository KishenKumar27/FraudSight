NATIVE_FUNC_MYSQL = """

-- Operators
>	Greater than operator	
>=	Greater than or equal operator	
<	Less than operator	
<>, !=	Not equal operator	
<=	Less than or equal operator	
%, MOD	Modulo operator	
*	Multiplication operator	
+	Addition operator	
-	Minus operator	
-	Change the sign of the argument	
/	Division operator	
:=	Assign a value	
=	Assign a value (as part of a SET statement, or as part of the SET clause in an UPDATE statement)	
=	Equal operator	

-- Functions
ABS()	Return the absolute value	
ADDDATE()	Add time values (intervals) to a date value	
ADDTIME()	Add time	
AND, &&	Logical AND	
ANY_VALUE()	Suppress ONLY_FULL_GROUP_BY value rejection	
ASCII()	Return numeric value of left-most character	
AVG()	Return the average value of the argument	
BETWEEN ... AND ...	Whether a value is within a range of values	
CASE	Case operator	
CAST()	Cast a value as a certain type	
CEIL()	Return the smallest integer value not less than the argument	
CEILING()	Return the smallest integer value not less than the argument			
COALESCE()	Return the first non-NULL argument	
COERCIBILITY()	Return the collation coercibility value of the string argument	
COLLATION()	Return the collation of the string argument		
CONCAT()	Return concatenated string	
CONCAT_WS()	Return concatenate with separator	
CONV()	Convert numbers between different number bases	
CONVERT()	Cast a value as a certain type		
COUNT()	Return a count of the number of rows returned	
COUNT(DISTINCT)	Return the count of a number of different values	
CUME_DIST()	Cumulative distribution value	
CURDATE()	Return the current date	
CURRENT_DATE(), CURRENT_DATE	Synonyms for CURDATE()	
CURRENT_ROLE()	Return the current active roles	
CURRENT_TIME(), CURRENT_TIME	Synonyms for CURTIME()	
CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP	Synonyms for NOW()	
CURRENT_USER(), CURRENT_USER	The authenticated user name and host name	
CURTIME()	Return the current time	
DATE()	Extract the date part of a date or datetime expression	
DATE_ADD()	Add time values (intervals) to a date value	
DATE_FORMAT()	Format date as specified	
DATE_SUB()	Subtract a time value (interval) from a date	
DATEDIFF()	Subtract two dates	
DAY()	Synonym for DAYOFMONTH()	
DAYNAME()	Return the name of the weekday	
DAYOFMONTH()	Return the day of the month (0-31)	
DAYOFWEEK()	Return the weekday index of the argument	
DAYOFYEAR()	Return the day of the year (1-366)	
DEFAULT()	Return the default value for a table column	
DENSE_RANK()	Rank of current row within its partition, without gaps	
DIV	Integer division	
ELT()	Return string at index number	
EXISTS()	Whether the result of a query contains any rows	
EXP()	Raise to the power of	
EXTRACT()	Extract part of a date	
ExtractValue()	Extract a value from an XML string using XPath notation	
FIRST_VALUE()	Value of argument from first row of window frame	
FLOOR()	Return the largest integer value not greater than the argument	
FORMAT()	Return a number formatted to specified number of decimal places	
FOUND_ROWS()	For a SELECT with a LIMIT clause, the number of rows that would be returned were there no LIMIT clause	
FROM_DAYS()	Convert a day number to a date	
FROM_UNIXTIME()	Format Unix timestamp as a date	
GET_FORMAT()	Return a date format string		
GREATEST()	Return the largest argument	
GROUP_CONCAT()	Return a concatenated string	
GROUPING()	Distinguish super-aggregate ROLLUP rows from regular rows	
HOUR()	Extract the hour	
IF()	If/else construct	
IFNULL()	Null if/else construct	
IN()	Whether a value is within a set of values		
INSERT()	Insert substring at specified position up to specified number of characters	
INSTR()	Return the index of the first occurrence of substring	
IS	Test a value against a boolean	
IS NOT	Test a value against a boolean	
IS NOT NULL	NOT NULL value test	
IS NULL	NULL value test		
ISNULL()	Test whether the argument is NULL	
LAG()	Value of argument from row lagging current row within partition	
LAST_DAY	Return the last day of the month for the argument	
LAST_VALUE()	Value of argument from last row of window frame	
LCASE()	Synonym for LOWER()		
LIKE	Simple pattern matching	
LOCALTIME(), LOCALTIME	Synonym for NOW()	
LOCALTIMESTAMP, LOCALTIMESTAMP()	Synonym for NOW()	
MAKE_SET()	Return a set of comma-separated strings that have the corresponding bit in bits set	
MAX()	Return the maximum value	
MIN()	Return the minimum value	
MOD()	Return the remainder	
MONTH()	Return the month from the date passed	
MONTHNAME()	Return the name of the month	
NAME_CONST()	Cause the column to have the given name	
NOT, !	Negates value	
NOT BETWEEN ... AND ...	Whether a value is not within a range of values	
NOT EXISTS()	Whether the result of a query contains no rows	
NOT IN()	Whether a value is not within a set of values	
NOT LIKE	Negation of simple pattern matching	
NOT REGEXP	Negation of REGEXP	
NOW()	Return the current date and time	
NULLIF()	Return NULL if expr1 = expr2	
OCTET_LENGTH()	Synonym for LENGTH()	
OR, ||	Logical OR		
PERCENT_RANK()	Percentage rank value	
PERIOD_ADD()	Add a period to a year-month	
PERIOD_DIFF()	Return the number of months between periods	
POSITION()	Synonym for LOCATE()	
QUARTER()	Return the quarter from a date argument	
RADIANS()	Return argument converted to radians	
RAND()	Return a random floating-point value	
RANK()	Rank of current row within its partition, with gaps	
REGEXP	Whether string matches regular expression	
REGEXP_INSTR()	Starting index of substring matching regular expression	
REGEXP_LIKE()	Whether string matches regular expression	
REGEXP_REPLACE()	Replace substrings matching regular expression	
REGEXP_SUBSTR()	Return substring matching regular expression	
ROUND()	Round the argument	
ROW_COUNT()	The number of rows updated	
ROW_NUMBER()	Number of current row within its partition	
RPAD()	Append string the specified number of times	
RTRIM()	Remove trailing spaces	
SQRT()	Return the square root of the argument		
STD()	Return the population standard deviation	
STR_TO_DATE()	Convert a string to a date	
STRCMP()	Compare two strings	
SUBDATE()	Synonym for DATE_SUB() when invoked with three arguments	
SUBSTR()	Return the substring as specified	
SUBSTRING()	Return the substring as specified	
SUBSTRING_INDEX()	Return a substring from a string before the specified number of occurrences of the delimiter	
SUBTIME()	Subtract times	
SUM()	Return the sum	
TIME()	Extract the time portion of the expression passed	
TIME_FORMAT()	Format as time	
TIMEDIFF()	Subtract time	
TIMESTAMP()	With a single argument, this function returns the date or datetime expression; with two arguments, the sum of the arguments	
TIMESTAMPADD()	Add an interval to a datetime expression	
TIMESTAMPDIFF()	Return the difference of two datetime expressions, using the units specified	
TO_DAYS()	Return the date argument converted to days	
TRUNCATE()	Truncate to specified number of decimal places	
UCASE()	Synonym for UPPER()	
UPPER()	Convert to uppercase	
VALUES()	Define the values to be used during an INSERT	
VAR_POP()	Return the population standard variance	
VAR_SAMP()	Return the sample variance	
WEEK()	Return the week number	
WEEKDAY()	Return the weekday index	
WEEKOFYEAR()	Return the calendar week of the date (1-53)	
YEAR()	Return the year	
"""