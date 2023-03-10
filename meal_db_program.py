from getpass import getpass
from mysql.connector import connect, Error

dbUser = "MYSQL_USERNAME"        #MySQL username
dbPasswd = "MYSQL_PASSWORD"   #MySQL password
programImagesDir = "C:/Users/PC/Desktop/meal_program/"  #This variable id used to store the direcotry that the image folder is in

def checkTablesFunc(cursor, table_name):
    check_table_query = """
    SELECT * FROM information_schema.TABLES
    WHERE
        TABLE_SCHEMA LIKE "meal_db" AND
        TABLE_TYPE LIKE "BASE TABLE" AND
    """
    check_table_query = check_table_query + 'TABLE_NAME = "'+str(table_name)+'"'

    cursor.execute(check_table_query)
    result = cursor.fetchall()

    print("Result = " + str(result))
    print("")

    if len(result) != 0:
        print(str(table_name) + " does exist")
        return True
    else:
        print(str(table_name + " doesn't exist"))
        return False



def checkMealDBFunc():
    try:
        mydb = connect(host="localhost", user = dbUser, password = dbPasswd)
        with mydb as connection:
            with connection.cursor() as cursor:
                check_mealDB_query = """
                SELECT * FROM information_schema.TABLES
                WHERE
                    TABLE_SCHEMA LIKE "meal_db"
                """

                cursor.execute(check_mealDB_query)
                result = cursor.fetchall()

                if len(result) == 0:
                    cursor.execute("CREATE DATABASE meal_db;")

                #cursor.execute("DROP DATABASE meal_db;")
        mydb.close()        #Closes the connection
    except Error as e:
        print("CheckMealDBFunc Error")
        print(e)



def ingredientsTableFunc(cursor):       #This function is responsible for creating and inserting data into the ingredients table
    create_ingredients_table_query = """
        CREATE TABLE ingredients(
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            name VARCHAR(50),
            is_liquid BOOLEAN,
            energy FLOAT,
            fat FLOAT,
            sat_fat FLOAT,
            carbs FLOAT,
            sugar FLOAT,
            fibre FLOAT,
            protein FLOAT,
            salt FLOAT,
            vit_a FLOAT,
            thiamin FLOAT,
            riboflavin FLOAT,
            niacin FLOAT,
            vit_b6 FLOAT,
            vit_b12 FLOAT,
            vit_c FLOAT,
            vit_d FLOAT,
            calcium FLOAT,
            phosphorus FLOAT,
            magnesium FLOAT,
            potassium FLOAT,
            iron FLOAT,
            zinc FLOAT,
            copper FLOAT,
            selenium FLOAT
        );
        """

    insert_ingredients_query = """
        INSERT INTO ingredients (name, is_liquid, energy, fat, sat_fat, carbs, sugar, fibre, protein, salt, vit_a, thiamin,
        riboflavin, niacin, vit_b6, vit_b12, vit_c, vit_d, calcium, phosphorus, magnesium, potassium, iron, zinc, copper, selenium)
        VALUES
            ("Chicken breast cooked(USDA)",false,148,3.39,1.01,0,0,0,29.5,0.215,10,0.079,0.227,11.1,0.984,0.2,0,0,6,249,31,420,0.43,0.82,0.034,42.4),
            ("Oil vegetable (USDA)",true,884,100,15.3,0,0,0,0,0,0,0,0,0,0,0,0,null,0,0,0,0,0.02,0,0,0),
            ("Onion yellow (USDA)",false,38,0.05,null,8.61,5.82,1.9,0.83,0.001,null,null,null,null,null,null,8.2,null,15,34,9,182,0.28,0.2,0.035,2.49),
            ("Apple granny smith (USDA)",false,59,0.14,null,14.1,10.6,2.5,0.27,0.0009,null,0.017,0.075,0.11,0.028,null,null,null,5,10,5.1,116,0.07,0.02,0.035,null),
            ("Garlic (USDA)",false,143,0.38,null,28.2,null,null,6.62,null,null,null,null,null,null,null,10,null,null,null,null,null,null,null,null,9.8),
            ("Korma paste (Tesco)",false,118,4.1,1,17.2,10.1,2.9,1.7,1.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Chicken stock liquid (Tesco)",true,6,0.3,0.2,0.5,0.2,0.1,0.3,0.8,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Rasins (Tesco)",false,330,1.1,0.2,74.5,62.4,4,3.6,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Sultanas (Tesco)",false,285,0.3,0.1,64.7,60.8,5.5,3.1,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Soft apricots (Tesco)",false,210,0.6,0.1,45.2,41.1,7.1,2.5,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Brown rice (USDA)",false,123,0.97,0.26,25.6,0.24,1.6,2.74,0.004,0,0.178,0.069,2.56,0.123,0,0,0,3,103,39,86,0.56,0.71,0.106,5.8),
            ("Corn flour (Tesco)",false,357,0.6,0,87.5,0,0,0.5,0.18,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Banana overripe (USDA)",false,85,0.22,null,20.1,15.8,1.7,0.73,null,1,0.04,0.09,0.57,0.234,null,9.7,null,null,null,null,null,null,null,null,null),
            ("Banana ripe (USDA)",false,98,0.29,null,23,15.8,1.7,0.74,0.0039,1,0.056,0.09,0.662,0.209,null,12.3,null,5,22,28,326,0.39,0.16,0.101,2.4),
            ("Plain greek yogurt (USDA)",false,94,4.39,2.39,4.75,3.25,null,8.78,0.034,38,0.055,0.244,0.227,0.044,null,null,0,111,126,10.7,147,0.09,0.47,0.01,null),
            ("Natural yogurt (Tesco)",false,83,3.8,2.6,6.8,5.9,0.4,5.2,0.14,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Coriander leaves (USDA)",false,23,0.52,0.014,3.67,0.87,2.8,2.13,0.046,337,0.067,0.162,1.11,0.149,0,27,0,67,48,26,521,1.77,0.5,0.225,0.9),
            ("Black pepper (USDA)",false,251,3.26,1.39,64,0.64,25.3,10.4,0.02,27,0.108,0.18,1.14,0.291,0,0,0,443,158,171,1330,9.71,1.19,1.33,4.9),
            ("Oil rapeseed (Tesco)",true,825,91.7,7.3,0,0,0,0,0,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Bell pepper red (USDA)",false,26,0.3,0.059,6.03,4.2,2.1,0.99,0.004,157,0.054,0.085,0.979,0.291,0,128,0,7,26,12,211,0.43,0.25,0.017,0.1),
            ("Bell pepper yellow (USDA)",false,27,0.21,0.031,6.32,null,0.9,1,0.002,10,0.028,0.025,0.89,0.168,0,184,0,11,24,12,212,0.46,0.17,0.107,0.3),
            ("Bell pepper green (USDA)",false,20,0.17,0.058,4.64,2.4,1.7,0.86,0.003,18,0.057,0.028,0.48,0.224,0,80.4,0,10,20,10,175,0.34,0.13,0.066,0),
            ("Green chilli (USDA)",false,40,0.2,0.021,9.46,5.1,1.5,2,0.007,59,0.09,0.09,0.95,0.278,0,242,0,18,46,25,340,1.2,0.3,0.174,0.5),
            ("Ginger (USDA)",false,80,0.75,0.203,17.8,1.7,2,1.82,0.013,0,0.025,0.034,0.75,0.16,0,5,0,16,34,43,415,0.6,0.34,0.226,0.7),
            ("Tomatoes tinned (USDA)",false,21,0.5,null,3.32,2.99,null,0.84,0.125,null,null,null,null,null,null,null,null,30,18,9.8,198,0.57,0.12,0.052,0),
            ("Mince turkey 2% (Tesco)",false,114,1.3,0.4,0.2,0.2,0.1,25.4,0.2,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Turmeric powder (USDA)",false,312,3.25,1.84,67.1,3.21,22.7,9.68,0.027,0,0.058,0.15,1.35,0.107,0,0.7,0,168,299,19.8,2080,55,4.5,1.3,6.2),
            ("Cumin seeds (USDA)",false,375,22.3,1.54,44.2,2.25,10.5,17.8,0.168,64,0.628,0.327,4.58,0.435,0,7.7,0,931,499,366,1790,66.4,4.8,0.867,5.2),
            ("Chilli powder (USDA)",false,282,14.3,2.46,49.7,7.19,34.8,13.5,2.87,1480,0.25,0.94,11.6,2.09,0,0.7,0,330,300,149,1950,17.3,4.3,1,20.4),
            ("Garam masala (Tesco)",false,356,17.2,1.1,19.5,0.5,35.4,13,0.13,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Coriander powder (Tesco)",false,346,17.8,1,13.1,0,41.9,12.4,0.08,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Water (USDA)",true,0,0,0,0,0,0,0,0.004,0,0,0,0,0,0,0,0,3,0,1,0,0,0.01,0.01,0),
            ("Flank steak (USDA)",false,263,16.4,6.92,0,0,0,27,0.07,0,0.14,0.18,4.42,0.35,3.3,0,null,6,256,23,337,3.33,5.77,0.119,30.4),
            ("Carrot cooked (USDA)",false,147,3,0.03,8.22,3.45,3,0.76,0.058,852,0.066,0.044,0.645,0.153,0,3.6,0,30,30,10,235,0.34,0.2,0.017,0.7),
            ("Curry powder (USDA)",false,325,14,1.65,55.8,2.76,53.2,14.3,0.052,1,0.176,0.2,3.26,0.105,0,0.7,0,525,367,255,1170,19.1,4.7,1.2,40.3),
            ("Mango chutney (Tesco)",false,234,0.4,0.1,56.6,52.4,1.4,0.2,2.5,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Tomato puree (USDA)",false,257,0.2,0.016,65.1,39,3.3,2.1,0.023,100,0.04,null,2.5,null,null,4.3,null,31,72,null,852,2.8,null,null,null),
            ("Rice white (USDA)",false,97,0.19,0.039,21.1,0.05,1,2.02,0.005,0,0.02,0.013,0.29,0.026,0,0,0,2,8,5,10,0.14,0.41,0.049,5.6),
            ("Cinnamon powder (USDA)",false,247,1.24,0.345,80.6,2.17,53.1,3.99,0.01,15,0.022,0.041,1.33,0.158,0,3.8,0,1000,64,60,431,8.32,1.83,0.339,3.1),
            ("Tomatoes cooked (USDA)",false,18,0.11,0.015,4.01,2.49,0.7,0.95,0.011,24,0.036,0.022,0.532,0.079,0,22.8,0,11,28,9,218,0.68,0.14,0.075,0.5),
            ("Chicken thigh (USDA)",false,232,14.7,4.11,0,0,0,23.3,0.102,16,0.088,0.19,5.79,0.414,0.44,0,0.2,9,216,22,253,1.08,1.73,0.063,25.3),
            ("Cumin powder (Tesco)",false,428,22.3,1.5,33.7,2.2,10.5,17.8,0.4,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Pineapple tinned (USDA)",false,52,0.12,0.009,13.4,12.6,0.8,0.36,0.001,2,0.091,0.025,0.292,0.074,0,7.5,0,14,7,16,105,0.39,0.12,0.103,0.4),
            ("Soy sauce low sodium (USDA)",true,57,0.3,0.035,5.59,0.5,0.7,9.05,3.6,0,0.04,0.24,1.14,0.16,0,0,0,30,166,69,352,1.35,0.79,0.049,0.5),
            ("Celery cooked (USDA)",false,18,0.16,0.04,4,2.37,1.6,0.83,0.091,26,0.023,0.07,0.372,0.086,0,6.1,0,42,25,12,284,0.42,0.14,0.036,1),
            ("Spring onion (USDA)",false,32,0.19,0.032,7.34,2.33,2.6,1.83,0.016,50,0.055,0.08,0.525,0.061,0,18.8,0,72,37,20,276,1.48,0.39,0.083,0.6),
            ("Courgette cooked (USDA)",false,15,0.36,0.072,2.69,1.71,1,1.14,0.003,56,0.035,0.024,0.51,0.08,0,12.9,0,18,37,19,264,0.37,0.33,0.052,0.2),
            ("Chinese 5 spice (Tesco)",false,332,11.5,0.6,28.5,0.6,31.7,12.7,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Ginger ground (USDA)",false,335,4.24,2.6,71.6,3.39,14.1,8.98,0.027,2,0.046,0.17,9.62,0.626,0,0.7,0,114,168,214,1320,19.8,3.64,0.48,55.8),
            ("Parsley fresh (USDA)",false,36,0.79,0.132,6.33,0.85,3.3,2.97,0.056,421,0.086,0.098,1.31,0.09,0,133,0,138,58,50,554,6.2,1.07,0.149,0.1),
            ("Celery (USDA)",false,14,0.17,0.042,2.97,1.34,1.6,0.69,0.08,22,0.021,0.057,0.32,0.074,0,3.1,0,40,24,11,260,0.2,0.13,0.035,0.4),
            ("Thyme Fresh (USDA)",false,101,1.68,0.467,24.4,null,14,5.56,0.009,238,0.048,0.471,1.82,0.348,0,160,0,405,106,160,609,17.4,1.81,0.555,null),
            ("Chillies red medium heat (Tesco)",false,20,0.6,0,0.7,0.7,0,2.9,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Lime juice (USDA)",true,21,0.23,0.026,6.69,1.37,0.4,0.25,0.016,1,0.033,0.003,0.163,0.027,0,6.4,0,12,10,7,75,0.23,0.06,0.03,0.1),
            ("Coley fish (Conish Fishmonger)",false,82,1,0.1,0,0,null,18.3,0.15,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Cod steamed (USDA)",false,87,0.52,0.107,0,0,0,19.2,0.445,2,0.033,0.051,1.17,0.118,2.21,0,0.6,10,318,23,251,0.2,0.39,0.024,28.8),
            ("Pollock cooked (USDA)",false,111,1.18,0.159,0,0,0,23.5,0.419,17,0.054,0.223,3.95,0.329,3.66,0,1.3,72,267,81,430,0.56,0.57,0.06,44.1),
            ("Cornmeal white (USDA)",false,398,5.04,0.853,77.1,1.46,10.4,11,0.004,null,0.31,0.137,2.8,0.583,null,0,null,11,280,125,443,3.79,3.24,0.219,null),
            ("Okra (USDA)",false,33,0.19,0.026,7.45,1.48,3.2,1.93,0.007,36,0.2,0.06,1,0.215,0,23,0,82,61,57,299,0.62,0.58,0.109,0.7),
            ("Chillies scotch bonnet (Sainsburys)",false,30,0.49,null,4.2,4,null,1.8,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Lemon juice (USDA)",true,17,0.07,0.027,5.66,1.59,0.7,0.47,0.026,2,0.02,0.017,0.18,0.037,null,16.6,null,9,9,6,109,0.06,0.23,0.018,null),
            ("Chicken drumsticks roasted (USDA)",false,191,10.2,2.74,0,0,0,23.4,0.123,12,0.093,0.203,5.4,0.383,0.39,0,0.1,11,195,22,247,1.11,2.36,0.071,26.9),
            ("Chicken drumsticks skinless roasted (USDA)",false,155,5.7,1.5,0,0,0,24.2,0.128,6,0.098,0.222,5.6,0.407,0.38,0,0,11,200,22,256,1.14,2.56,0.074,28.1),
            ("Potatoes boiled without skin (USDA)",false,360,0.1,0.026,20,0.89,2,1.71,0.241,0,0.098,0.019,1.31,0.269,0,7.4,0,8,40,20,328,0.31,0.27,0.167,0.3),
            ("Peas frozen cooked (USDA)",false,78,0.27,0.049,14.3,4.4,4.5,5.15,0.072,105,0.283,0.1,1.48,0.113,0,9.9,0,24,77,22,110,1.52,0.67,0.105,1),
            ("Milk semi skimmed not fortified (USDA)",true,50,1.98,1.26,4.8,5.06,0,3.3,0.047,28,0.039,0.185,0.092,0.038,0,0.2,0,120,92,11,140,0.02,0.48,0.006,2.5),
            ("Aubergine cooked (USDA)",false,35,0.23,0.044,8.73,3.2,2.5,0.83,0.001,2,0.076,0.02,0.6,0.086,0,1.3,0,6,15,11,123,0.25,0.12,0.059,0.1),
            ("Potatoes boiled with skin (USDA)",false,78,0.1,0.026,17.2,null,3.3,2.86,0.014,0,0.032,0.036,1.22,0.239,0,5.2,0,45,54,30,407,6.07,0.44,0.878,0.3),
            ("Shallots (USDA)",false,72,0.1,0.017,16.8,7.87,3.2,2.5,0.012,0,0.06,0.02,0.2,0.345,0,8,0,37,60,21,334,1.2,0.4,0.088,1.2),
            ("Peanuts unsalted (USDA)",false,567,49.2,6.28,16.1,4.72,8.5,25.8,0.018,0,0.64,0.135,12.1,0.348,0,0,0,92,376,168,705,4.58,3.27,1.14,7.2),
            ("Chickpea flour (USDA)",false,387,6.69,0.693,57.8,10.8,10.8,22.4,0.064,2,0.486,0.106,1.76,0.492,0,0,0,45,318,166,846,4.86,2.81,0.912,8.3),
            ("Garlic paste (Tesco)",false,76,0.2,0.1,13.3,7.8,2.4,4,1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Ginger paste (Tesco)",false,42,0.4,0.1,7.6,2.6,2.4,0.8,1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Kidney beans red boiled (USDA)",false,127,0.5,0.072,22.8,0.32,7.4,8.67,0.002,0,0.16,0.058,0.578,0.12,0,1.2,0,28,142,45,403,2.94,1.07,0.242,1.2),
            ("All purpose seasoning (Tesco)",false,847,9.7,1,6.6,1,null,12,39,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Coconut milk light (Tesco)",true,61,6,5.2,1.3,0.8,0,0.4,0.009,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Tofu (Tesco)",false,118,7.1,1.2,1,0.7,1.9,13,0.03,null,null,null,null,null,null,null,null,401,null,null,null,null,null,null,null),
            ("Paprika (USDA)",false,282,12.9,2.14,54,10.3,34.9,14.1,0.068,2460,0.33,1.23,10.1,2.14,0,0.9,0,229,314,178,2280,21.1,4.33,0.713,6.3),
            ("Jamaican curry powder (Tropical Sun Food)",false,399,11.7,null,52,null,23.2,9.9,0.11,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Thyme dried (USDA)",false,276,7.43,2.73,63.9,1.71,37,9.11,0.055,190,0.513,0.399,4.94,0.55,0,50,0,1890,201,220,814,124,6.18,0.86,4.6),
            ("Vegetable stock liquid (Tesco)",true,7,0.4,0.09,0.7,0.5,0.09,0.2,0.7,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Bay leaf (USDA)",false,313,8.36,2.28,75,null,26.3,7.61,0.023,309,0.009,0.421,2,1.74,0,46.5,0,834,113,120,529,43,3.7,0.416,2.8),
            ("Sweet potato boiled without skin (USDA)",false,76,0.14,0.031,17.7,5.74,2.5,1.37,0.027,787,0.056,0.047,0.538,0.165,0,12.8,0,27,32,18,230,0.72,0.2,0.094,0.2),
            ("Tortilla wholemeal wrap (Tesco)",false,279,5.2,2.5,45.7,3.3,6.9,9,0.9,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Cheese cheddar extra mature low fat (Tesco)",false,314,22.1,13.8,0.8,0.1,0,27.9,1.8,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Mushrooms white cooked (USDA)",false,29,0.33,0.04,4.04,0,1.8,3.58,0.012,0,0.096,0.463,3.99,0.042,0,0,0.2,4,105,11,396,0.25,0.57,0.291,13.9),
            ("Mixed salad (Tesco) ",false,18,0.4,0.1,1.3,1.1,2.3,1.2,0.02,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Carrot (USDA) ",false,41,0.24,0.032,9.58,4.74,2.8,0.93,0.069,835,0.066,0.058,0.983,0.138,0,5.9,0,33,35,12,320,0.3,0.24,0.045,0.1),
            ("Italian seasoning (Buy Whole Foods Online)",false,310,17.55,3.21,38.11,null,21.16,11.89,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Basil fresh (USDA)",false,23,0.64,0.041,2.65,0.3,1.6,3.15,0.004,264,0.034,0.076,0.902,0.155,0,18,0,177,56,64,295,3.17,0.81,0.385,0.3),
            ("Haddock cooked (USDA)",false,90,0.55,0.111,0,0,0,20,0.261,21,0.023,0.069,4.12,0.327,2.13,0,0.6,14,278,26,351,0.21,0.4,0.026,31.7),
            ("Leek cooked (USDA)",false,31,0.2,0.027,7.62,2.11,1,0.81,0.01,41,0.026,0.02,0.2,0.113,0,4.2,0,30,17,14,87,1.1,0.06,0.062,0.5),
            ("Ham wafer thin (Tesco)",false,105,2.5,0.9,1.1,1,1,19,1.52,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Flour plain (Tesco)",false,349,0.5,0.09,74.3,2.9,3.2,10.1,0.13,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Buttery spread low fat (Tesco)",false,290,31,7,null,1,null,null,1.2,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Mustard wholegrain (Tesco)",false,198,12.3,1.8,6.6,5.4,7.5,11.5,3.3,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Mince beef 5% (Tesco)",false,124,4.5,2,0,0,0,20.8,0.28,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Bread wholemeal (USDA)",false,254,2.98,0.732,43.1,4.41,6,12.3,0.45,null,0.391,0.166,4.43,0.216,null,null,null,163,212,76.6,250,2.56,1.76,0.226,25.8),
            ("Egg cooked (USDA)",false,155,10.6,3.27,1.12,1.12,0,12.6,0.124,149,0.066,0.513,0.064,0.121,0,0,2.2,50,172,10,126,1.19,1.05,0.013,30.8),
            ("Onion red (USDA)",false,44,0.1,null,9.93,5.76,3.97,0.94,0.001,null,null,null,null,null,null,8.1,null,17,41,11.4,197,0.24,0.17,0.058,0.5),
            ("Lettuce iceberg (USDA)",false,14,0.14,0.018,2.97,1.97,1.2,0.9,0.01,25,0.041,0.025,0.123,0.042,0,2.8,0,18,20,7,141,0.41,0.15,0.025,0.1),
            ("Bread roll wholemeal (Tesco)",false,239,3.4,0.8,38.7,4.6,5,11,0.67,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Tomato (USDA)",false,18,0.2,0.028,3.89,2.63,1.2,0.88,0.005,42,0.037,0.019,0.594,0.08,0,13.7,0,10,24,11,237,0.27,0.17,0.059,0),
            ("Green beans cooked (USDA)",false,35,0.28,0.064,7.88,3.63,3.2,1.89,0.001,32,0.074,0.097,0.614,0.056,0,9.7,0,44,29,18,146,0.65,0.25,0.057,0.2),
            ("Mixed herbs (Buy Whole Foods Online)",false,340,7.7,null,63.4,null,null,11.8,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Gravy granules reduced salt (Tesco)",false,411,15.8,11,64.9,18,1.8,1.5,8.45,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Sweetcorn cooked (USDA)",false,94,0.74,0.114,22.3,3.59,2.8,3.11,0.004,12,0.174,0.069,1.52,0.224,0,4.8,0,3,75,29,251,0.61,0.63,0.046,0.7),
            ("Flour wholemeal (Tesco)",false,350,2.6,0.5,65,1.4,10,12,0.03,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Baking powder (USDA)",false,53,0,0,27.7,0,0.2,0,10.6,0,0,0,0,0,0,0,0,5880,2190,27,20,11,0.01,0.01,0.2),
            ("Bicarbonate of soda (Pink Sun)",false,0,0,0,0,0,0,0,27,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Greek style yogurt low fat (Tesco)",false,75,2.6,1.7,7.2,7,0.5,5.4,0.18,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Mint fresh (Tesco)",false,43,0.7,0.2,5.3,0,0,3.8,0.04,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Sweet potato cooked with skin (USDA)",false,90,0.15,0.052,20.7,6.48,3.3,2.01,0.036,961,0.107,0.106,1.49,0.286,0,19.6,0,38,54,0.497,475,0.69,0.32,0.161,0.2),
            ("Brown mustard seeds (Buy Whole Foods Online)",false,508,36.24,1.99,28.09,6.79,12.2,26.08,0.03,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Fennel seeds (USDA)",false,345,14.9,0.48,52.3,null,39.8,15.8,0.088,7,0.408,0.353,6.05,0.47,0,21,0,1200,487,385,1690,18.5,3.7,1.07,null),
            ("Nigella seeds (Tesco)",false,434,30.6,4.8,1.4,1.4,36.1,20.3,0.07,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Fenugreek seeds (USDA)",false,323,6.41,1.46,58.4,null,24.6,23,0.067,3,0.322,0.366,1.64,0.6,0,3,0,176,296,191,770,33.5,2.5,1.11,6.3),
            ("Black eyed beans cooked (Tesco)",false,127,0.7,0.2,18.2,1,6.5,8.8,0.01,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Plantain ripe cooked (USDA)",false,155,0.16,0,41.4,21.3,2.2,1.52,0.002,45,0.09,0.13,0.685,0.21,0,16.4,0,3,37,41,477,0.28,0.21,0.044,0),
            ("Salt table (USDA)",false,0,0,0,0,0,0,0,38.8,0,0,0,0,0,0,0,0,24,0,1,8,0.33,0.1,0.03,0.1),
            ("Pizza base (Tesco)",false,259,3.1,1.1,48.4,2.7,3.1,7.9,0.28,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Cheese mozzarella (USDA)",false,296,17.8,11.7,4.44,1.81,null,23.7,0.699,203,0.023,0.36,0.101,0.09,1.65,null,null,693,533,27.2,116,0.2,3.62,0.035,26.7),
            ("Bread crumbs plain (USDA)",false,395,5.3,1.2,72,6.2,4.5,13.4,732,0,0.967,0.403,6.63,0.121,0.35,0,0,183,165,43,196,4.83,1.45,0.255,25.2),
            ("Mushy peas (Tesco)",false,72,0.4,0.09,11.5,1.3,2.8,4.3,0.4,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Butter unsalted (USDA)",false,717,81.1,50.5,0.06,0.06,0,0.85,0.011,684,0.005,0.034,0.042,0.003,0,0,0,24,24,2,24,0.02,0.09,0.016,1),
            ("Butter salted (USDA)",false,717,81.1,51.4,0.06,0.06,0,0.85,0.643,684,0.005,0.034,0.042,0.003,0.17,0,0,24,24,2,24,0.02,0.09,0,1),
            ("Ghee (USDA)",false,900,100,null,0,0,0,0,0,null,null,null,null,null,null,null,null,0,null,null,null,0,null,null,null),
            ("Baked beans (Tesco)",false,85,0.6,0.1,12.5,4.7,5.9,4.6,0.6,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Oregano dried (USDA)",false,265,4.28,1.55,68.9,4.09,42.5,9,0.025,85,0.177,0.528,4.64,1.04,0,2.3,0,1600,148,270,1260,36.8,2.69,0.633,4.5),
            ("Mixed spice (Tesco)",false,372,12.7,4.8,47.7,4.9,20.4,6.4,0.13,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("All spice ground (Tesco)",false,348,8.7,2.6,50.5,0,21.6,6.1,0.19,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Onion granules (Tesco)",false,362,1.1,0.2,75,35.5,5.7,10.1,0.3,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Cayenne pepper ground (USDA)",false,318,17.3,3.26,56.6,10.3,27.2,12,0.03,2080,0.328,0.919,8.7,2.45,0,76.4,0,148,293,152,2010,7.8,2.48,0.373,8.8),
            ("Sumac (Tesco)",false,324,16.6,3.9,17.6,1.3,44.6,3.8,3.13,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Sesame seeds toasted (USDA)",false,565,48,6.72,25.7,null,14,17,0.011,0,0.803,0.251,4.58,0.802,0,0,0,989,638,356,475,14.8,7.16,2.47,34.4),
            ("Apple gala (USDA)",false,57,0.12,null,13.7,10.4,2.3,0.25,0.001,1,0.017,0.029,0.075,0.049,null,null,null,7,11,5,108,0.12,0.05,0.021,0),
            ("Oil olive (USDA)",false,884,100,13.8,0,0,0,0,0.002,0,0,0,0,0,0,0,0,1,0,0,1,0.56,0,0,0),
            ("Jerk seasoning (Tesco)",false,285,5.4,1.3,34.9,13.8,null,10.2,8.25,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Sweetcorn on cob (USDA)",false,94,0.74,0.114,22.3,null,2.1,3.11,0.004,0,0.174,0.069,1.52,0.224,0,4.8,0,3,75,29,251,0.61,0.63,0.046,0.7),
            ("Haddock smoked (USDA)",false,116,0.96,0.173,0,0,0,25.2,0.763,24,0.047,0.049,5.07,0.4,0,0,0.8,49,251,54,415,1.4,0.5,0.042,42.9),
            ("Salmon farmed atlantic cooked (USDA)",false,206,12.4,2.4,0,0,0,22.1,0.061,69,0.34,0.135,8.04,0.647,2.8,3.7,13.1,15,252,30,384,0.34,0.43,0.049,41.4),
            ("Pasta macaroni (USDA)",false,128,0.11,0.016,26.6,1.15,4.3,4.53,0.006,5,0.112,0.061,1.07,0.024,0,0,0,11,50,19,31,0.49,0.44,0.092,19.8),
            ("Mustard english (Tesco)",false,183,10.2,1.4,14.9,11.8,3.5,6.2,7.3,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Chillies rocket (Tesco)",false,64,0.6,0.1,10.7,4.5,2.5,2.6,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Mustard seeds (USDA)",false,508,36.2,1.99,28.1,6.79,12.2,26.1,0.013,2,0.805,0.261,4.73,0.397,0,7.1,0,266,828,370,738,9.21,6.08,0.645,208),
            ("Oil mustard (USDA)",false,884,100,11.6,0,null,0,0,0,0,0,0,0,0,0,0,null,0,0,0,0,0,0,0,0),
            ("Broccoli cooked (USDA)",false,35,0.41,0.079,7.18,1.39,3.3,2.38,0.041,77,0.063,0.123,0.553,0.2,0,64.9,0,40,67,21,293,0.67,0.45,0.061,1.6),
            ("Spinach (USDA)",false,29,0.57,0.041,4.21,0.65,2.9,3.63,0.074,586,0.094,0.224,0.507,0.172,0,5.5,0,129,49,75,346,1.89,0.56,0.144,6),
            ("Butternut squash (USDA)",false,39,0.07,0.014,10,null,null,1.23,0.002,167,0.05,0.039,0.464,0.069,0,3.5,0,19,14,9,133,0.58,0.12,0.036,0.5),
            ("Mince quorn (Tesco)",false,92,1.7,0.5,2.3,0.1,7.5,13,0.14,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Pasta unenriched cooked (USDA)",false,158,0.93,0.176,30.9,0.56,1.8,5.8,0.001,0,0.02,0.02,0.4,0.049,0,0,0,7,58,18,44,0.5,0.51,0.1,26.4),
            ("Pine nuts (USDA)",false,673,68.4,4.9,13.1,3.59,3.7,13.7,0.002,1,0.364,0.227,4.39,0.094,0,0.8,0,16,575,251,597,5.53,6.45,1.32,0.7),
            ("Pesto red reduced fat (Tesco)",false,247,20.7,3.3,8.4,5.6,4,4.8,0.96,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Rice arbotio (CalorieKing)",false,283,0.8,0.3,61,1.3,0,7,0.013,null,null,null,null,null,null,null,null,null,null,null,38,null,null,null,null),
            ("Swede cooked (USDA)",false,30,0.18,0.029,6.84,3.95,1.8,0.93,0.005,0,0.082,0.041,0.715,0.102,0,18.8,0,18,41,10,216,0.18,0.12,0.029,0.7),
            ("Sausages reduced fat (Tesco)",false,241,15.6,6.1,6.2,0.7,1,18.5,1.2,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Spinach baby (USDA)",false,27,0.62,null,2.41,null,1.6,2.85,0.111,283,0.077,0.194,0.551,0.195,null,26.5,null,68,39,92.9,582,1.26,0.45,0.082,2.51),
            ("Lentils red split (Tesco)",false,96,0.8,0.1,11.7,0.1,6.1,7.3,0.1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Moong beans split (Bazaar Foods)",false,311,1.1,0.3,46.3,1.5,10,23.9,0.04,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Pasta spaghetti cooked (USDA)",false,130,0.63,0.091,26.2,null,null,4.58,0.014,8,0.097,0.103,1.53,0.096,0,0,0,30,108,62,58,1.04,1.08,0.205,22.1),
            ("Bacon back unsmoked (Tesco)",false,200,14.8,5.6,0.3,0.2,0.5,16.2,2.8,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Cheese soft reduced fat garlic and herb (Tesco)",false,163,11,7.6,6.4,3.6,0.2,9.6,0.5,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Basil dried (USDA)",false,233,4.07,2.16,47.8,1.71,37.7,23,0.076,37,0.08,1.2,4.9,1.34,0,0.8,0,2240,274,711,2630,89.8,7.1,2.1,3),
            ("Cheese cream low fat (USDA)",false,208,16.7,10,6.73,3.3,0,7.85,0.317,161,0.04,0.185,0.125,0.045,0.92,0,0.3,148,152,8,247,0.17,0.57,0.032,4),
            ("Turkey breast meat only cooked (USDA)",false,147,2.08,0.593,0,0,0,30.1,0.099,3,0.035,0.205,11.8,0.807,0.39,0,0.3,9,230,32,249,0.71,1.72,0.063,30.2),
            ("Potatoes baked with skin (USDA)",false,198,0.1,0.026,46.1,1.4,7.9,4.29,0.021,1,0.122,0.106,3.06,0.614,0,13.5,0,34,101,43,573,7.04,0.49,0.817,0.7),
            ("Chicken whole roasted with skin (USDA)",false,215,12,3.02,0.02,0.02,0,26.9,0.411,18,0.062,0.218,5.92,0.181,0.51,0,null,21,255,25,291,1.07,2.63,0.084,34.8),
            ("Cabbage savoy cooked (USDA)",false,24,0.09,0.012,5.41,null,2.8,1.8,0.024,44,0.051,0.02,0.024,0.152,0,17,0,30,33,24,184,0.38,0.23,0.052,0.7),
            ("Cheese parmesan (USDA)",false,392,25,14.8,3.22,0.11,0,35.8,1.18,207,0.039,0.332,0.271,0.091,1.2,0,0.5,1180,694,44,92,0.82,2.75,0.032,22.5),
            ("Cheese soft reduced fat (Tesco)",false,161,11,7.6,5.4,3.9,0.7,9.7,0.42,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Lemon zest (CarbManager)",false,47,0,0,17,5,10,1.7,0.007,15,null,null,null,0,0,128,0,133,12,15,160,1.7,0,0,0),
            ("Chives (USDA)",false,20,0.73,0.146,4.35,1.85,2.5,3.27,0.003,218,0.078,0.115,0.647,0.138,0,58.1,0,92,58,42,296,1.6,0.56,0.157,0.9),
            ("Beans cannellini tinned (USDA)",false,79,0.17,0.039,14.9,null,4.8,4.93,0.336,0,0.055,0.034,0.261,0.091,0,0,0,21,74,39,220,1.81,0.65,0.18,4.5),
            ("Sage ground (USDA)",false,315,12.8,7.03,60.7,1.71,40.3,10.6,0.011,295,0.754,0.336,5.72,2.69,0,32.4,0,1650,91,428,1070,28.1,4.7,0.757,3.7),
            ("Chickpeas tinned (USDA)",false,139,2.77,0.214,22.5,4.01,6.4,7.05,0.246,1,0.027,0.015,0.14,0.116,0,0.1,0,45,85,26,126,1.07,0.63,0.253,3.1),
            ("Sweetcorn baby (Tesco)",false,42,0.3,0.2,6.4,5,2.6,2,0.01,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Beef diced (USDA)",false,191,6.82,2.8,0,0,0,32.4,0.067,2,0.075,0.25,4.12,0.511,0,0,0.1,16,228,23,319,2.96,8.32,0.12,34.6),
            ("Flour self raising (Tesco)",false,348,0.4,0.1,74.6,1.6,3,10,0.65,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Tuna tinned in water (USDA)",false,128,2.97,0.792,0,null,0,23.6,0.05,6,0.008,0.044,5.8,0.217,1.17,0,null,14,217,33,237,0.97,0.48,0.039,65.7),
            ("Bap large white (Tesco)",false,255,2.6,0.7,47.7,4.4,3.3,8.4,0.86,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Egg yolk (USDA)",false,322,26.5,9.55,3.59,0.56,0,15.9,0.048,381,0.176,0.528,0.024,0.35,1.95,0,5.4,129,390,5,109,2.73,2.3,0.077,56),
            ("Noodles egg cooked (USDA)",false,132,1.57,0.361,24.2,0.71,2.3,5.04,0.012,10,0.245,0.123,1.47,0.114,0.14,0,0.1,19,57,24,37,1.09,0.63,0.08,21.8),
            ("Orange fruit (USDA)",false,46,0.21,0.025,11.5,9.14,2.4,0.7,0,11,0.1,0.04,0.4,0.051,0,45,0,43,12,10,169,0.09,0.08,0.039,0.5),
            ("Orange juice (USDA)",false,45,0.2,0.024,10.4,8.4,0.2,0.7,0.001,10,0.09,0.03,0.4,0.04,0,50,0,11,17,11,200,0.2,0.05,0.044,0.1),
            ("Parsnip cooked (USDA)",false,71,0.3,0.05,17,4.8,4,1.32,0.246,0,0.083,0.051,0.724,0.093,0,13,0,37,69,29,367,0.58,0.26,0.138,1.7),
            ("Cauliflower cooked (USDA)",false,23,0.45,0.07,4.11,2.08,2.3,1.84,0.015,1,0.042,0.052,0.41,0.173,0,44.3,0,16,32,9,142,0.32,0.17,0.018,0.6),
            ("Lentils red (USDA)",false,358,2.17,0.379,63.1,null,10.8,23.9,0.007,3,0.51,0.106,1.5,0.403,0,1.7,0,48,294,59,668,7.39,3.6,1.3,0),
            ("Jalfrezi curry paste (Tesco)",false,285,24.3,3.7,7.8,1.1,null,3.2,4.8,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null),
            ("Rice brown long grain (USDA)",false,123,0.97,0.26,25.6,0.24,1.6,2.74,0.004,0,0.178,0.069,2.56,0.123,0,0,0,3,103,39,86,0.56,0.71,0.106,5.8),
            ("Beetroot cooked (USDA)",false,44,0.18,0.028,9.96,7.96,2,1.68,0.077,2,0.027,0.04,0.331,0.067,0,3.6,0,16,38,23,305,0.79,0.35,0.074,0.7),
            ("Worcestershire sauce (USDA)",true,77,0,0,19.2,10,0,0,1.3,5,0.07,0.13,0.7,0,0,13,0,107,60,13,800,5.3,0.19,0.2,0.5),
            ("Tomatoes cherry (Tesco)",false,17,0.1,0,2.9,2.9,1,0.5,0.01,null,null,null,null,null,null,22,null,null,null,null,null,null,null,null,null),
            ("Vinegar distilled (USDA)",true,18,0,0,0.04,0.04,0,0,0.002,0,0,0,0,0,0,0,0,6,4,1,2,0.03,0.01,0.006,0.5),
            ("Mayonnaise low fat (USDA)",false,238,22.2,3.45,9.23,3.56,0,0.37,0.827,8,0.008,0,0.01,0.002,0,0,0,6,15,2,31,0.14,0.07,0.019,2.6),
            ("Beef roast deli style (USDA)",false,115,3.69,1.32,0.64,0.29,0,18.6,0.853,3,0.043,0.213,5.58,0.46,0,0,0,5,242,20,647,2.05,3.2,0.086,14.7);
        """

    cursor.execute(create_ingredients_table_query)
    cursor.execute(insert_ingredients_query)



def mealsTableFunc(cursor):     #This function is responsible for creating and inserting data into the meals table
    create_meals_table_query = """
        CREATE TABLE meals(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            num_servings TINYINT,
            instructions TEXT,
            img_dir TINYTEXT
        );
        """

    insert_meals_query = ('INSERT INTO meals (id, name, num_servings, instructions, img_dir)'
        + 'VALUES'
        + '''(1,"Chicken and banana korma", 4, "1. Heat the vegetable oil in a large saucepan. Add the chicken, onion, apple and garlic, and cook for 2 to 3 minutes, stirring often. Add the curry paste and cook for a few seconds, stirring. ^^2. Add thestock, raisins (or sultanas) and apricots. Bring to the boil, then reduce the heat and simmer, partially covered, for 35 minutes. Add a little more stock or water, if necessary. ^^3. Brown rice takes 30 to 35 minutes to cook, so put it in plenty of simmering water. ^^4. Just before serving, blend the cornflour with 2 tbsp cold water and add to the curry, stirring until thickened. Slice in the banana, cooking gently for another few moments. Check the seasoning, adding pepper, if needed. ^^5. Serve, topping each portion with 1 tablespoon of yoghurt and accompanied with the rice. Garnish with coriander, if using.", "''' + programImagesDir + '''images/chicken_and_banana_korma_img.jpg"),'''
        + '''(2,"Chicken jalfrezi", 4, "1. Heat the oil in a non-stick pan on a high heat. Add the chicken pieces and cook for 2 minutes. Add the cumin, turmeric, chilli powder and half a teaspoon of salt (if using). Mix well and fry on a medium heat for 3 to 4 mins, stirring frequently to stop the mixture from catching, until the chicken is lightly cooked and starting to turn white. ^^2. Remove the chicken and set aside, leaving the oil and juices in the pan. Fry the sliced onions on a medium heat for 7 minutes, until they're soft and beginning to turn golden. While the onions are cooking, blend the tinned tomatoes in a blender, or mash well using a masher or the back of a fork. ^^3. Add the ginger, garlic and peppers to the pan and cook for 2 minutes, then add the tomatoes, mix well and cook for another 2 minutes. Stir in the coriander powder, chilli powder, garam masala, cumin seeds and half a teaspoon of salt (if using), and cook for a further minute. ^^4. Add the chicken pieces back to the pan, stir well to coat in the mixture and cook for a couple of minutes. Add the green chillies, mix and fry on medium heat for another 2 minutes. Pour the water into the pot and stir, then cover and simmer on low heat for 10 to 15 minutes. ^^5. Once the chicken is tender and the sauce has thickened, turn off the heat and scatter over the chopped coriander.", "''' + programImagesDir + '''images/chicken_jalfrezi.jpg"),'''
        + '''(3,"Beef curry", 4, "1. Brown the beef in a large saucepan or flameproof casserole dish over a low heat. Add the onion and cook for 5 minutes, stirring occasionally. ^^2. Add the peppers, carrots and garlic. Cook for 5 minutes, stirring often to stop it from sticking, adding a little water if necessary. ^^3. Add the curry powder and stir well to mix, then add the tomatoes, mango chutney, 300ml water and the tomato pur??e. Cover and simmer gently for between 90 minutes and 2 hours, or until the meat is tender, adding more water if necessary. ^^4. About 15 minutes before serving, cook the rice according to packet instructions. Serve with the curry.", "''' + programImagesDir + '''images/beef_curry.jpg"),'''
        + '''(4,"Bariis iskukaris", 4, "1. Heat the oil in a large saucepan, and gently fry the onions and garlic on medium heat for 2 minutes. Add the cinnamon stick (or ground cinnamon), cumin seeds and chopped tomatoes, and cook for 3 minutes on medium heat, stirring frequently. ^^2. Add the chicken, turmeric, cumin powder, coriander, crumbled seasoning cube and grated carrot. Mix well and cook on medium-high heat for about 5 minutes, stirring regularly. ^^3. Add 400ml water, cover the pot and leave to cook on medium heat for 15 minutes, until the chicken is nearly done. ^^4. Add the rice and stir until it's well coated by the mixture. Add in another 200ml of cold water, stir, then cover the pot and cook on medium-high heat until it starts bubbling (about 5 minutes or so). Once it's bubbling, reduce the heat to low and leave to steam until the rice grains are tender and fluffy ??? around 10 to 15 minutes. ^^5. Once ready, serve topped with fresh coriander (if you want) and accompanied by a fresh green salad.", "''' + programImagesDir + '''images/bariis_iskukaris.jpg"),'''
        + '''(5,"Sweet and sour chicken", 4, "1. Put the brown rice on to cook in plenty of boiling water for 30 minutes, or until tender. ^^2. Meanwhile, drain the juice from the pineapple into a small bowl or jug, and cut the pineapple rings into chunks. Add the cornflour to the juice and stir until smooth, then mix in the tomato pur??e and soy sauce. Set aside. ^^3. When the rice is 10 minutes from being ready, heat the oil in a wok or very large frying pan. Add the chicken and stir-fry over a high heat for 3 to 4 minutes. ^^4. Add the onion, pepper and celery to the pan. Stir-fry for another 3 to 4 minutes, then add the tomato wedges and pineapple chunks. ^^5. Give the pineapple juice mixture a quick stir, then add pan. Keep stirring until the sauce is hot and thickened. Season with the pepper, and serve with the drained rice.", "''' + programImagesDir + '''images/sweet_and_sour_chicken.jpg"),'''
        + '''(6, "Bajan cou cou with spicy fish", 4, "Marinade^60g fresh coriander^35g fresh parsley^2 stalks celery, roughly chopped^3 spring onions, chopped^5 garlic cloves^half a small onion^2.5cm (1 inch) chunk of fresh ginger, peeled^4 sprigs thyme^4 red mild chillis^2 teaspoons lime juice^650g white fish fillets (such as coley, cod or pollock), cleaned and washed^^Fish sauce^1 tablespoon vegetable oil^1 small onion, sliced^half a yellow pepper, deseeded and cut into strips^half a red pepper, deseeded and cut into strips^2 sprigs fresh thyme^400g tin chopped tomatoes^1 small scotch bonnet pepper, finely chopped (optional)^0.5 teaspoon salt (optional)^^Cou cou^200g cornmeal powder^100g raw okra, diced^1 teaspoon vegetable oil^600ml water^^1.Add the parsley, celery, spring onion, onion, ginger, 4 sprigs of fresh thyme, red chilli and lime juice to a food processor and pulse several times to give a coarse green marinade. Put the fish fillets in a bowl, then pour in the mixture. Turn and brush the fish well to make sure it's completely covered by the marinade. Cover the bowl and put it in the fridge for at least 30 minutes (or even overnight).^^2. To make the sauce, heat the oil in a large pan and add the onions and peppers. Cook for about 5 minutes on medium heat until they have started to soften and turn golden. Then add the remaining 2 sprigs of thyme and the scotch bonnet (if using), and cook for 1 more minute. Add the marinated fish, tomatoes and salt, gently stir and spoon the sauce over the fish. Turn the heat down to low, cover the pot and simmer for 10 to 15 minutes.^^3. While the fish is cooking, make the cou cou. Add the cornmeal to a mixing bowl and slowly add just enough cold water to cover it. Use a wooden spoon to mix to a smooth paste, with no dry lumps visible. Set this cornmeal paste aside.^^4. Put the diced okra in a pot with about 400ml of water. Bring to a medium boil, then lower the heat and leave to simmer for about 5 minutes until the okra softens. Use a sieve or colander to drain the okra, making sure to keep the hot okra water. Put the okra aside, then pour about a quarter of the hot okra water back into the pan and the rest into a jug.^^5. With the heat on low, gradually add a quarter of the soaked cornmeal mixture to the okra water in the pot, and whisk to a smooth paste. Add the oil to the mixture and whisk well, before gradually adding the rest of the okra water and cornmeal. Whisk continuously until all the cornmeal and liquid is well mixed and smooth.^^6. Switch to a wooden spoon and keep mixing the cornmeal for another 2 or 3 minutes. It will start to bubble and thicken, so will need mixing harder to avoid lumps. At this point add the cooked okra and mix for another few minutes, or until the okra is well incorporated though the cornmeal, and then remove from the heat (For softer cou cou, add more boiled water at this stage).^^7. Scatter the chopped parsley over the fish, and serve with the cou cou.", "''' + programImagesDir + '''images/bajan_cou_cou_with_spicy_fish.jpg"),'''
        + '''(7, "Bang tasty chicken drumsticks", 4, "1. Put the tomato pur??e, reduced-salt soy sauce and lemon juice into a mixing bowl (not a metal one). Mix well and season with black pepper. Add the chicken drumsticks, turning to coat them in the mixture. Cover and refrigerate for at least 30 minutes, or overnight if preferred.^^2. When ready to cook, preheat the oven to 200C/fan oven 180C/gas mark 6. Arrange the drumsticks in a foil-lined roasting tin and roast for 30 minutes, brushing them with the remaining glaze after 20 minutes.^^3. While the chicken is roasting, boil the potatoes and carrots in separate saucepans until tender ??? they will take about 20 minutes. Put the peas on to cook in a little boiling water, 5 minutes before the chicken is ready.^^4. Drain and mash the potatoes, beat in the milk and season with black pepper. Serve with the chicken drumsticks, carrots and peas.", "''' + programImagesDir + '''images/bang_tasty_chicken_drumsticks.jpg"),'''
        + '''(8, "Bharelu shaak", 4, "Vegetables^4 small aubergines^6 okra fingers^4 new potatoes^4 long Turkish peppers, slit into halves and de-seeded^3 shallot onions^^Stuffing mixture^2 tablespoons unsalted peanuts, crushed^4 tablespoons gram flour^1.5 tablespoons vegetable oil^1 teaspoon garam masala^1 teaspoon garlic paste^0.5 teaspoon salt (optional)^1 teaspoon ginger paste^3 chillies, crushed^0.5 teaspoon turmeric powder^0.5 teaspoon cumin powder^0.5 teaspoon coriander powder^chopped fresh coriander, to serve^^1. Pre-heat the oven to 200C (180C fan, gas mark 5). In a deep baking tray, add a small drop of oil and 240ml water. Using a knife, make slits in all the vegetables, deep and long enough to allow enough space for stuffing them.^^2. In a separate bowl, combine all the ingredients for the stuffing and mix well. Then stuff a few spoonfuls of the mixture into each vegetable.^^3. Place the stuffed vegetables into the oiled tray. If you have any of the stuffing mixture leftover, sprinkle it over the top, then cover with foil, and bake in the oven for 40 minutes or until the potatoes are soft.^^4. Once ready, take out of the oven and leave to cool for a few minutes before serving.", "''' + programImagesDir + '''images/bharelu_shaak_gujurati_stuffed.jpg"),'''
        + '''(9, "Carribbean tofu and sweet potato curry", 4, "Rice and peas^125g dried kidney beans, soaked overnight and rinsed ^1 medium onion, chopped^2 spring onions, cut in half^2 sprigs fresh thyme ^1 scotch bonnet pepper^1 teaspoon black pepper^1 teaspoon all-purpose seasoning^1 garlic clove, finely chopped^100ml low-fat/light coconut milk^125g white rice (long grain or basmati), washed and drained  ^^Curry^300g extra-firm tofu, patted dry and cut into 2.5cm cubes^3 teaspoons vegetable oil^1 medium onion, chopped^4 garlic cloves, crushed and minced^0.5 teaspoon turmeric powder^1 teaspoon paprika^2 teaspoons Jamaican curry powder^0.5 scotch bonnet pepper, deseeded and chopped^0.5 teaspoon dried thyme^1 low-salt seasoning cube (5g)^1 bay leaf^125g sweet potatoes, peeled and chopped into bite-sized chunks^3 spring onions, chopped^2 tablespoons fresh coriander to garnish, chopped^^1. Put the beans in a large pot. Add the onions, fresh thyme, spring onions, chopped garlic, black pepper, all-purpose seasoning, whole scotch bonnet and coconut milk. Cover with 400ml of water, stir and then boil on a medium-low heat for 40 to 50 minutes, until the beans are soft. (You can cut the cooking time by using tinned beans instead of dried ??? just add all the ingredients, skip the initial boiling and go straight to adding the rice)^^2. Add the washed rice to the beans and mix together. There should be about 2.5cm (1 inch) of water above the rice and beans ??? add more if needed, then cover the pot and cook on a low heat for 30 minutes or until the rice is tender. While the rice is cooking, start on the curry.^^3. Heat 2 teaspoons of oil in a large non-stick pan or wok. Add the tofu and fry on each side until golden. Once cooked, remove the tofu cubes and drain on a plate lined with a paper towel to soak up any oil.^^4. Heat the remaining teaspoon of oil in the same pan. Add the onions, garlic and pepper, and cook on medium heat for a couple of minutes, then add the turmeric, paprika, curry powder, scotch bonnet, dried thyme, crushed seasoning cube and bay leaf. Stir well to combine, and cook for another minute or 2 before adding the sweet potato and mixing thoroughly.^^5. Add about 500ml of water, then bring to the boil on medium heat. Once boiling, cover and lower the heat to a simmer for 10 to 12 minutes, until the sweet potatoes are soft and the curry has thickened.^^6. Add the spring onion and tofu cubes to the curry, then bring back to the boil and cook for a further 5 minutes. Once the curry is ready, carefully remove the scotch bonnet from the cooked rice and peas, and fluff the rice with a fork. Serve with a portion of the curry, scattered with the fresh coriander.", "''' + programImagesDir + '''images/caribbean_tofu_and_sweet_potato.jpg"),'''
        + '''(10, "Cheats pizza calzone", 4, "1. Preheat the grill. Arrange the peppers and mushrooms on a baking sheet and grill them for 4 to 5 minutes, turning once. Add the tomatoes and herbs, then season with black pepper. Keep warm. (Add some torn-up basil leaves to the tomato mixture)^^2. Put a tortilla into a dry frying pan and sprinkle a quarter of the cheese over the top. Cook over a medium heat for about 30 to 40 seconds until melted.^^3. Add a quarter of the vegetable mixture to one side of the tortilla, then fold it in half, over the filling. Cook for a few moments, then slide it onto a warm serving plate. Keep warm.^^4. Repeat with the remaining tortillas. Serve with the salad leaves, grated carrot and celery.", "''' + programImagesDir + '''images/cheats_pizza_calzone.jpg"),'''
        + '''(11, "Cheese and tomato grilled fish", 4, "1. Preheat the grill to medium-high. Grease a baking sheet with the vegetable oil.^^2. Arrange the fish fillets on the baking sheet and spread 1 tablespoon of the tomato pur??e over each one. Top with the tomatoes, season with a little pepper and scatter the grated cheese on top.^^3. Grill for 6 to 8 minutes, until the fish is cooked. The flesh should flake easily when tested with a fork. Serve with fresh green vegetables, and cooked rice or boiled potatoes.", "''' + programImagesDir + '''images/cheese_and_tomato_grilled_fish.jpg"),'''
        + '''(12, "Cheesy ham and leek bake", 4, "1. Cook the leeks in a large saucepan of simmering water for 10 to 12 minutes, until just tender, then drain well in a colander. It helps if you leave them for a few minutes to cool slightly too.^^2. Wrap a slice of ham around each leek, then arrange them in a large shallow baking dish. Turn on the oven to preheat to 200C (fan 180, gas mark 6).^^3. Put the flour, low-fat spread and milk into a non-stick saucepan. Heat, stirring all the time with a small whisk until the sauce is thick and smooth. Cook gently for a few seconds more, then remove from the heat.^^4. Add all but 1 tablespoon of the cheese to the pan, then stir in the mustard, season with some pepper and keep stirring until the cheese has all melted. Add sliced tomatoes on top of the leeks before pouring the whole mixture over the leeks, then sprinkle the remaining cheese over the top.^^5. Bake in the oven for 15 to 20 minutes, until the leeks are heated through and the top is golden brown. Leave to cool for a few minutes, then plate up.", "''' + programImagesDir + '''images/cheesy_leeks_and_ham_bake.jpg"),'''
        + '''(13, "Chicken and vegetable parcels", 4, "1. Cut 4 pieces of greaseproof paper or baking parchment, each measuring approximately 30cm square. Put each chicken breast onto a separate square of greaseproof paper.^^2. Mix the vegetables together and place an equal amount on top of each piece of chicken. Sprinkle with 5-spice powder (if using), the ginger, soy sauce and black pepper.^^3. Fold up the paper to wrap up the chicken completely. Put the parcels into a steamer, cover and steam for 35 to 40 minutes.^^4. Check that the chicken is properly cooked by unwrapping one of the parcels and inserting a sharp knife into the thickest part. The juices should run clear with no traces of pink. (It's important when steaming to make sure the water never boils dry. Check from time to time and top up with extra boiling water if needed.)^^5. Serve the chicken in the parcel", "''' + programImagesDir + '''images/chicken_and_vegetable.jpg"),'''
        + '''(14, "Chilli beef and bean burger", 4, "Burgers^1 small onion, quartered^small can (about 210g) red kidney beans, drained and rinsed^250g lean beef mince^wholemeal breadcrumbs (from 1 slice of bread)^2 teaspoons mild chilli powder, or to taste^1 egg, beaten^1 tablespoon tomato pur??e^^To serve^1 extra large tomato, sliced^1 red onion, sliced^lettuce leaves^4 wholemeal rolls^^1. Chop the onion in a food processor, then add the beans, mince, breadcrumbs, chilli powder, beaten egg and tomato pur??e, and mix again.(If you prefer a chunkier texture, mash the beans with a fork or potato masher, chop the onions by hand and then mix with the other ingredients.)^^2. Shape the mixture into 4 patties and chill until you're ready to cook.^^3. Barbecue or grill for 5 to 7 minutes each side.^^4. Serve in the rolls, with sliced onion and tomato, and lettuce leaves.", "''' + programImagesDir + '''images/chilli_beef_and_bean_burgers.jpg"),'''
        + '''(15, "Chilli con carne", 4, "1. Heat a large saucepan and add the minced beef, a handful at a time, cooking it until browned. Add the onion and garlic, then cook for another 2 to 3 minutes.^^2. Add the chopped tomatoes, tomato pur??e, spices, red pepper, mushrooms, kidney beans and stock. Stir well, bring to the boil, then lower the heat and simmer gently for 15 to 20 minutes.^^3. Meanwhile, cook the rice according to pack instructions.^^4. Season the chilli with pepper and serve with the boiled rice.", "''' + programImagesDir + '''images/chilli_con_carne.jpg"),'''
        + '''(16, "Classic cottage pie", 4, "1. Cook the potatoes in a large saucepan of boiling water for about 20 minutes until tender.^^2. While the potatoes are cooking, heat a large saucepan. Add the minced beef a handful at a time, cooking until browned.^^3. Stir in the onion, carrot, courgette, green beans and mixed herbs, then add 450ml water. Bring to the boil, then turn down the heat and simmer without a lid for about 20 minutes, until the veg has softened.^^4. Turn the grill on to preheat, and warm a large baking dish under it for a couple of minutes. While the grill is heating, drain and mash the potatoes, seasoning them with some pepper.^^5. Add the sweetcorn to the mince mixture, then sprinkle in the gravy granules and stir until thickened. Season if needed, then tip into the baking dish. Spoon the mash on top, spreading it out to cover the mince, then pop under the grill.^^6. Once the top has browned, remove from the grill and leave to cool for a couple of minutes. Dish up and enjoy!", "''' + programImagesDir + '''images/classic_cottage_pie.jpg"),'''
        + '''(17, "Corn frizzlers", 4, "Fritters^180g plain or wholemeal flour^1.5 teaspoons baking powder^0.5 teaspoon bicarbonate of soda^4 eggs^250ml semi-skimmed milk^2 spring onions, sliced^350g sweetcorn^1 large sweet potato, grated^1 teaspoon curry powder^1 tablespoon oil^0.5 red chilli, de-seeded and sliced^1 handful of fresh coriander, roughly chopped^^Yoghurt dip^250g low-fat plain Greek-style yoghurt^10g of fresh mint, finely chopped^2 pinches black pepper^^1. Mix the flour and baking powder in a bowl. Add the eggs and milk, and whisk until the mixture becomes a smooth batter. Then stir in the corn, sweet potato, spring onions, curry powder, and chilli and coriander if using.^^2. Heat the oil in a pan over a medium heat. Add a few tablespoons of batter to the pan, making sure each dollop has enough space around it and does not overlap with the others. Fry the fritters for 2 to 3 minutes on each side, or until golden and cooked through.^^3. Once the fritters are ready, remove from the pan onto a plate lined with kitchen paper. Work in batches until all the batter is cooked.^^4. Make the dip by mixing the yoghurt, mint and pepper together in a bowl. Serve alongside the fritters and get dipping! Add a side salad and a crusty wholemeal roll to make a light meal.", "''' + programImagesDir + '''images/corn_frizzlers.jpg"),'''
        + '''(18, "Deresh curry", 4, "Panch phoran^3.2g cumin seeds^3.2g brown mustard seeds^3.2g fennel seeds^3.2g nigella seeds^1.4g teaspoons fenugreek seeds^^1. Heat the vegetable oil in a pan, then add the panch phoran, bay leaves, chopped onion, garlic and ginger. Cook on low heat for 3 or 4 minutes, until the mixture starts to brown.^^2. Add the chopped potato, cover and cook for 5 minutes until it starts to soften.^^3. Add the okra and mix well. Add the water, stir and lower the heat. Leave the mixture to simmer uncovered for around 5 minutes, until the okra is softened", "''' + programImagesDir + '''images/deresh_curry.jpg"),'''
        + '''(19, "Ewa oloyin with plantain", 4, "1. To make the ewa oloyin, first bring 700ml of water to the boil in a large saucepan. Add the beans and half the onion, then cover and cook on medium-low heat for about 40 minutes. Check whether they're ready by crushing a few beans with the back of a fork ??? they should be easy to mash. If not, add more water (200ml at a time) and check again in another 10 minutes.^^2. Add the rest of the onion to the pot along with the oil, ground pepper and salt. Stir well and allow to cook for a further 5 minutes on low heat. Add the chopped bell pepper, stir and simmer for another few minutes, before turning off the heat and leaving to cool until it's time to serve.^^3. About 10 minutes before the beans are ready, steam the pieces of plantain until soft when pricked with a fork (about 12 to 15 minutes). Serve in a bowl with a ladle of beans and enjoy.", "''' + programImagesDir + '''images/ewa_oloyin_with_plantain.jpg"),'''
        + '''(20, "Fabulous fish pie", 4, "1. Boil the potatoes for 15 to 20 minutes until tender, then drain them and mash with 2 tablespoons of the milk.^^2. While the potatoes are boiling, preheat the oven to 200C (fan 180C, gas mark 6). Put the remaining milk, low-fat spread and flour into a saucepan. Bring to the boil over a medium heat, stirring continuously with a small whisk or wooden spoon until the sauce bubbles and thickens. Stir in the parsley and the peas, and season with pepper. Turn off the heat.^^3. Place the chunks of fish in an ovenproof dish. Pour the sauce over, then spoon the mashed potato on top, spreading it evenly. Finally, sprinkle the cheese over the whole dish.^^4. Bake in the centre of the oven for 25 to 30 minutes, until the top is golden brown.", "''' + programImagesDir + '''images/fabulous_fish_pie.jpg"),'''
        + '''(21, "Four seasons pizza", 4, "1. Preheat the oven to 200C (fan 180C, gas mark 6). Place the pizza base on a large baking sheet. Spoon the tomato pur??e on top and spread it evenly over the surface.^^2. Arrange the tomatoes on top. Scatter with half the mozzarella, then sprinkle with the herbs. Arrange the ham over a quarter of the pizza, along with the pineapple pieces.^^3. Arrange the mushrooms over a second quarter of the pizza. Put the cooked chicken or turkey over a third quarter of the pizza. Leave the last quarter as it is.^^4. Sprinkle the rest of the mozzarella over the whole pizza, then bake for 12 to 15 minutes until the cheese is bubbling. Let cool for a few moments before slicing and serving.", "''' + programImagesDir + '''images/four_seasons_pizza.jpg"),'''
        + '''(22, "Good old fish and chips", 4, "1. Preheat the oven to 200C (fan 180C, gas mark 6). Lightly grease a baking sheet with a little vegetable oil.^^2. Put the potato wedges into a roasting tin. Add the remaining vegetable oil and toss to coat. Season with black pepper. Transfer to the oven to bake for 35 to 40 minutes, turning them over after 20 minutes. (Not peeling the potatoes means you get more fibre in your diet ??? and they're quicker to prepare.)^^3. Meanwhile, sprinkle the breadcrumbs onto a large plate. Season with a little pepper. Dip each fish fillet in the beaten egg, then coat in the breadcrumbs. Place on the baking sheet, then transfer to the oven when you turn the potatoes, so that it cooks for 15 to 20 minutes. To check that the fish is cooked, it should flake easily when tested with a fork.^^4. Heat the mushy peas in a saucepan, then serve with the fish and chips.", "''' + programImagesDir + '''images/good_old_fish_and_chips.jpg"),'''
        + '''(23, "Jerk style chicken skewers", 4, "1. Mix the garlic, lemon juice and olive oil with 1 teaspoon of jerk seasoning (or 2 if you prefer a spicier flavour). Stir in the chicken and set aside while you prepare the vegetables.^^2. Thread a piece of pepper onto a skewer, then onion, then chicken, finishing with onion.^^3. Cook on the barbecue for 8 to 10 minutes, turning frequently. Alternatively, cook under a preheated grill.^^4. Meanwhile cook the sweetcorn cobettes in boiling water, or on the barbecue for 6 to 8 minutes.", "''' + programImagesDir + '''images/jerk_style_chicken_skewers.jpg"),'''
        + '''(24, "Kedgeree with a kick", 4, "1. Cook the rice in boiling water until tender, according to packet instructions. At the same time, hard-boil the eggs for 10 minutes.^^2. Put the chunks of fish into a large frying pan and add a little water. Heat and simmer for 3 to 4 minutes until the fish is opaque. Drain.^^3. Shell the eggs and quarter them. Drain the rice and add it to the fish with the curry powder, peas and parsley. Heat, stirring gently, for 2 to 3 minutes. Season with black pepper and serve, topped with the eggs", "''' + programImagesDir + '''images/kedgeree_with_a_kick.jpg"),'''
        + '''(25, "Mac and veg slices", 4, "1. Cook the macaroni in boiling water for 10 to 12 minutes, until just tender. Rinse with cold water to cool it quickly, then drain thoroughly.^^2. Heat the vegetable oil in a non-stick frying pan and stir-fry the pepper for 3 to 4 minutes. Remove from the heat and add the courgette and frozen peas or sweetcorn. Add the macaroni and mix well.^^3. Beat the eggs and milk together, then stir in the reduced-fat cheese and dried herbs. Season with black pepper. Pour into the frying pan and cook over a low heat for 4 to 5 minutes, without stirring, to set the base. Meanwhile, preheat the grill to medium-high.^^4. Put the frying pan under the grill and cook for 4 to 5 minutes until the surface has set and is golden brown. Serve hot, warm, or cold, cut into wedges ??? with some salad on the side.", "''' + programImagesDir + '''images/mac_and_veg_slices.jpg"),'''
        + '''(26, "Macaroni cheese with tomatoes", 4, "1. Preheat the oven to 190C (fan 170C, gas mark 5). Cook the macaroni in a large saucepan of boiling water for 8 to 10 minutes, or according to the instructions on the packet, until tender. Once it's ready, drain well and return it to the saucepan.^^2. While the pasta is cooking, melt the low-fat spread in a large saucepan and cook the onion for 3 or 4 minutes until softened, but not brown. Remove from the heat and stir in the flour a little at a time. Return to the heat and cook gently, stirring constantly, for about 1 minute, until the mixture has a texture a bit like sand. Remove from the heat again and add in the milk a little at a time, stirring well to mix together.^^3. Once all the milk is added, return to the heat once more. Stir the sauce constantly for a few minutes until it's thick and smooth. At this point, remove from the heat and add about two-thirds of the cheese and the mustard. Season with pepper, and stir again to combine.^^4. Add the hot cheese sauce to the pan with the cooked pasta and mix well to combine and coat everything with the sauce. Tip the mixture into a baking dish which can hold about 1.2 litres, or use individual serving dishes. Top with the tomato slices and sprinkle the remaining cheese on top.^^5. Pop in the oven and bake for 15 to 20 minutes until piping hot and the cheese on top is starting to brown. Remove from the oven, leave to cool for a couple of minutes and then serve.", "''' + programImagesDir + '''images/macaroni_cheese_with_tomatoes.jpg"),'''
        + '''(27, "Macher jhol", 4, "1. Put the fish steaks in a bowl with the turmeric powder and a pinch of salt. Mix well and set aside for later.^^2. In a blender or mixing bowl, blend the tomatoes, garlic, 3 green chilies, mustard seeds powdered, pinch of salt and 120ml water to a smooth paste. Keep aside.^^3. Heat 2 tablespoons mustard oil in a pan. Add the kalonji seeds and let sizzle for about 10 seconds, then add the blended tomato mixture. Turn the heat down to low, and stir for 8 minutes or so.^^4. Once the mixture has got a deeper, darker colour, add 350ml of water, stir well and bring to a boil. Once it's boiling, turn the heat back down to simmer on low for another 10 minutes.^^5. Heat 2 tablespoons of mustard oil in a pan, and then fry the marinated fish steaks until golden brown on both sides. Add the fish to the tomato mixture and leave to simmer for 2 or 3 minutes.^^6. Top with chopped coriander leaves and serve hot.", "''' + programImagesDir + '''images/macher_jhol.jpg"),'''
        + '''(28, "Mean and green mac and cheese", 6, "1. Cook the pasta in a pan of boiling water, according to the packet instructions ??? about 10 minutes. About 5 minutes before the pasta is cooked, add half the broccoli florets to the pan. Once ready, drain the pasta and broccoli and tip them into a casserole dish or roasting tin.^^2. To make the sauce, melt the spread in a saucepan over a medium heat. Add the flour and whisk quickly until it creates a paste, then add a small amount of the milk and whisk. Once the mixture is smooth, add a little more milk and keep whisking until smooth. Repeat until all the milk is in.^^3. Turn up the heat and bring the mixture to the boil. Mix in the mustard, ground cumin, spinach, peas and remaining 8 florets of broccoli, then lower the heat and let simmer for 5 to 10 minutes. While it's simmering, pre-heat the oven to 200C (180C fan, gas mark 6).^^4. Pour the sauce over the macaroni and broccoli, mix well until everything is covered, and spread evenly across the dish. Sprinkle over the breadcrumbs if using, and then bake in the pre-heated oven for 20 to 25 minutes, or until golden and bubbling. When it's ready, remove from the oven and leave to cool for 5 minutes ??? then plate up and tuck in!", "''' + programImagesDir + '''images/vegetable_mac_and_cheese.jpg"),'''
        + '''(29, "Meat free cottage pie", 4, "1. Cook the potatoes and butternut squash in a large saucepan of boiling water until tender, for about 20 minutes.^^2. Meanwhile, heat the vegetable oil in a large saucepan and gently fry the onion, garlic and carrots for 2 to 3 minutes, until softened. Add the vegetarian mince, tomatoes and stock. Stir in the curry powder, then add the mushrooms and courgette. Bring to the boil, then reduce the heat and cook, stirring occasionally, for 15 to 20 minutes. Season with black pepper.^^3. Preheat the grill, warming a large baking dish underneath for a few moments. Meanwhile, drain and mash the potatoes and butternut squash, seasoning with black pepper.^^4. Blend the cornflour with 1 tbsp cold water and add it to the mince mixture, stirring until thickened. Transfer it to the warm baking dish and spoon the vegetable mash on top. Grill for about 8 to 10 minutes, until browned. Serve.", "''' + programImagesDir + '''images/meat_free_cottage_pie.jpg"),'''
        + '''(30, "Meatballs and sauce", 4, "1. Mix some of the chopped onion and garlic with the mince. Shape the mince into small balls about half the size of a golf ball.^^2. Heat the oil in a non-stick frying pan and brown the meatballs on all sides. Remove and put on to a plate.^^3. Add the remaining onion to the frying pan and cook for 2 to 3 minutes until soft. Add the remaining garlic and cook for another minute.^^4. Add the tomatoes, tomato pur??e, herbs, mushrooms and peppers to the pan with 150ml water. Bring to the boil, then add the meatballs. Reduce the heat, cover with a lid and simmer for 30 minutes.^^5. About 10 minutes before serving, put the pasta on to cook in plenty of boiling water. Serve with the meatballs and tomato sauce.", "''' + programImagesDir + '''images/meatballs_and_sauce.jpg"),'''
        + '''(31, "Mediterrameam potato tray bake", 4, "1. Preheat the oven to 200C (180C fan, gas mark 6).^^2. Put the potatoes, chopped vegetables and pine nuts in a large roasting tin. Drizzle with the oil and toss to coat. Bake for 20 minutes, or until tender.^^3. Add the pesto and bake for another 5 minutes. Serve immediately.", "''' + programImagesDir + '''images/mediterranean_potato_bake.jpg"),'''
        + '''(32, "Mushroom risotto", 4, "1. Heat the vegetable oil in a large frying pan or saucepan, and cook the spring onions over a medium-high heat for a few seconds. Turn the heat down, then add the rice and fry over a low heat for about a minute, stirring all the time, until it looks glossy but not brown.^^2. Add the garlic and mushrooms, and cook for a minute, until the garlic is fragrant. Pour in about half the hot stock and stir well. Cook over a medium heat for 20 to 25 minutes, stirring often and slowly adding the remaining stock a little at a time, until the rice has soaked up all the liquid.^^3. Check that the rice is tender ??? it should have a nice creamy texture. If it needs cooking for a little longer, add a little more hot water and check again after another few minutes.^^4. Add the peas, stirring gently to mix them in. Cook for another couple of minutes to allow them to warm through and then serve.", "''' + programImagesDir + '''images/mushroom_risotto.jpg"),'''
        + '''(33, "Old school sausage and mash", 4, "1. Cook the carrots, swede and potatoes in a large saucepan of gently boiling water for about 20 minutes, until tender.^^2. Meanwhile, preheat the grill. Arrange the sausages on the grill rack and start to cook them when the vegetables have been cooking for 10 minutes. Grill them for 10 to 12 minutes, turning often.^^3. At the same time, start to make the red onion gravy. Heat the vegetable oil in a large non-stick frying pan and add the onion, cooking until soft and lightly browned ??? about 3 to 4 minutes.^^4. Pour in the stock and water, add the herbs, then simmer for 4 to 5 minutes. Add the blended cornflour and stir until thickened. Keep hot over a low heat.^^5. Drain and mash the vegetables, seasoning with black pepper. Serve 2 sausages per person with the red onion gravy.", "''' + programImagesDir + '''images/old_school_sausage_and_mash.jpg"),'''
        + '''(34, "Pakistani saag aloo", 4, "1. Heat the oil in a pan. Add the cumin seeds, chopped onion and garlic, and fry until softened and starting to brown.^^2. Add the chopped tomatoes and green chillies, and cook for another minute. Turn the heat down, add the cumin powder and turmeric, mix well and fry for a further minute.^^3. Add the potato, and then the spinach a minute or 2 later. Stir well to coat the potato and spinach in the spices, then cover the pan and leave to cook on low for 10 to 15 minutes, until the potato is soft. Stir occasionally to avoid sticking.^^4. Remove the lid and turn the heat up. Once the rest of the water has evaporated, turn off the heat and leave to cool for a few minutes.", "''' + programImagesDir + '''images/pakistani-saag-aloo.jpg"),'''
        + '''(35, "Panjabi dhal", 4, "1. Put the washed mung dhal and red lentils in a large pot, add the water and put on the hob on a low heat. After a few minutes, add the salt and turmeric, stir and bring to the boil. Once boiling, turn the heat down again and leave to simmer, partially covered, for around 15 minutes. (Reduce the cooking time by soaking the lentils in cold water for 3 or 4 hours before.)^^2. Meanwhile, heat the rapeseed oil in a shallow frying pan on medium heat. Add the cumin seeds and fry for 15 seconds, then add the onions and garlic. Once those are soft and beginning to brown (around 5 minutes), add the green chillies, mix well and cook for a further couple of minutes.^^3. Add the mixture from the frying pan to the simmering lentils, stir well and turn up to a medium heat. Once boiling, turn off the heat and remove the pot.^^4. Allow to cool for a few minutes, then top with chopped coriander.", "''' + programImagesDir + '''images/panjabi_dhal.jpg"),'''
        + '''(36, "Panjabi keema", 4, "1. Blend the chopped tomatoes, ginger and green chillies together, and set aside for later.^^2. Heat the oil in a non-stick pan on medium heat and cook the chopped onions for 5 minutes or so. Once softened and beginning to brown, add the chopped garlic and cook for a further 3 minutes.^^3. Add the blended tomato, ginger and chilli mix to the pan, along with the turmeric and frozen peas. Stir well and cook for a further 3 minutes.^^4. Add the turkey mince to the pan along with the remaining spices. Mix well and keep cooking on a medium heat until the meat has turned white. Cover the pan, turn the heat to low and cook for another 5 minutes.^^5. Remove the lid and carry on cooking for a few minutes to allow any excess water to evaporate. Once ready, top with chopped coriander.", "''' + programImagesDir + '''images/panjabi_keema.jpg"),'''
        + '''(37, "Pasta carbonara", 4, "1. Bring a large saucepan of water to the boil. Add the pasta and cook for 8 to 12 minutes, according to packet instructions.^^2. Meanwhile, heat the oil in a large non-stick frying pan. Add the bacon and spring onions, and cook for about 5 minutes, stirring often. Remove from the heat.^^3. Beat together the soft cheese and egg in a mixing bowl, then stir in the cooked bacon and spring onions. Add the milk, half the hard cheese and the parsley. Season with pepper.^^4. Drain the pasta and return it to the saucepan. Add the egg mixture and heat gently for 2 to 3 minutes, stirring constantly until the mixture thickens. Serve sprinkled with the remaining hard cheese.", "''' + programImagesDir + '''images/pasta_carbonara.jpg"),'''
        + '''(38, "Pasta ratatouille bake", 4, "1. Preheat the oven to 180C (160C fan, gas mark 4).^^2. Cook the macaroni according to pack instructions, then drain. Meanwhile, heat the oil in a large saucepan, then cook the onion and garlic slowly until tender and golden.^^3. Stir in the herbs, tomatoes, courgettes, beans and stock. Simmer for 5 minutes.^^4. Combine the pasta and vegetables, and season with black pepper. Transfer to a baking dish and sprinkle the cheese on top. Bake for 30 to 35 minutes.", "''' + programImagesDir + '''images/pasta_ratatouille_bake.jpg"),'''
        + '''(39, "Pea poppin risotto", 6, "1. Heat the oil in a frying pan over a medium-high heat. Cook the onions until they are soft and beginning to go see-through, stirring regularly. Add the garlic and cook for another minute.^^2. Tip the rice into the pan and cook for 2 minutes, then pour in a ladle of stock and keep stirring!^^3. Once the first ladle of stock is absorbed, pour in another and carry on cooking, stirring regularly. Repeat until the the rice is cooked and all but 200ml of the stock is used ??? about 20 minutes. Turn off the heat and set the pan aside.^^4. Put the spinach and half of the peas in a bowl, and add the remaining stock. Blend or mash until you have a smooth green sauce.^^5. Pour the green sauce into the rice, along with the remaining peas, fresh mint and lower-fat cream cheese. Stir well to mix, and put back on the heat for a couple of minutes to warm through. Serve topped with the grated lower-fat hard cheese and spoons at the ready!", "''' + programImagesDir + '''images/pea_poppin_risotto.jpg"),'''
        + '''(40, "Peppers with spicy turkey stuffing", 4, "1. Preheat the oven to 190C/fan 170C/gas mark 5. Arrange the peppers in a roasting pan, cut side up.^^2. Bring a large saucepan of water to a simmer, add the rice and cook for 12 to 15 minutes, or according to pack instructions, until tender.^^3. While the rice is cooking, heat the vegetable oil in a large frying pan or wok and stir-fry the onion and garlic for about 3 minutes, until softened. Add the turkey and stir-fry for about 5 minutes. Add the tomatoes, peas, paprika and herbs, then remove from the heat.^^4. Drain the rice, stir it thoroughly into the tomato mixture and season with some pepper. Spoon the filling into the pepper halves ??? it's fine if there's too much, just spoon the rest into the roasting pan!^^5. Cover with foil, bake for 20 to 25 minutes and then serve.", "''' + programImagesDir + '''images/peppers_with_spicy_turkey_stuffing.jpg"),'''
        + '''(41, "Perfect pasta and tomato sauce", 4, "1. Heat the oil in a saucepan or frying pan. Add the onion and cook over a medium heat for 3 to 4 minutes, until soft.^^2. Add the garlic, and cook gently for another minute. Add the chopped tomatoes, tomato pur??e and mixed herbs. Season with pepper and then simmer gently, stirring every now and again, for 15 minutes or until the sauce is thick and rich.^^3. After the sauce has been simmering for 8 to 10 minutes, start cooking the spaghetti according to pack instructions.^^4. Drain the spaghetti and serve with the sauce, topped with fresh basil or other chopped herbs, if you like.", "''' + programImagesDir + '''images/perfect_pasta_and_tomato_sauce.jpg"),'''
        + '''(42, "Roast chicken breast with peppers", 4, "1. Preheat the oven to 190C (fan 170C, gas mark 5). Put the potatoes onto the top shelf of the oven to bake.^^2. Heat the vegetable oil in a flame-proof casserole dish and stir-fry the onion and peppers over a high heat until softened, about 3 minutes.^^3. Put the paprika, herbs and flour into a shallow dish, and season with some pepper, stirring to mix. Dip each chicken breast into the mixture, coating them on both sides. Transfer them to the casserole dish, placing them on top of the onions and peppers.^^4. Pour in the stock, then cover the dish. Put in the oven to cook once the potatoes have been baking for 30 minutes. Bake for 35 minutes.^^5. Around 10 minutes before the chicken and potatoes are ready, cook the broccoli in boiling water for 8 to 10 minutes, drain and serve with the rest of the meal.", "''' + programImagesDir + '''images/roast_chicken_breasts_with_peppers.jpg"),'''
        + '''(43, "Roast dinner", 6, "1. Preheat the oven to 190C (170C fan, gas mark 5). Put the chicken into a large roasting tin and roast in the centre of the oven for 90 minutes.^^2. Put the potatoes into a separate roasting tin and add the oil. Toss to coat, then roast on the oven shelf above the chicken for 60 minutes, turning after 30 minutes.^^3. Start to cook the vegetables when the chicken is almost done. The carrots will take 10 to 15 minutes. The leeks, cabbage and peas will take 5 to 8 minutes when cooked together in a covered saucepan with a small amount of boiling water.^^4. Check that the chicken is completely cooked by piercing the thickest part of the leg with a sharp knife or skewer ??? the juices should be clear if the chicken is done. Transfer to a carving board and cover the chicken with foil, allowing it to rest for 10 minutes before carving.^^5. While the chicken is resting, make the gravy according to the pack instructions.^^6. Serve 150g of chicken per portion, without skin. Serve with the roast potatoes, vegetables and gravy.", "''' + programImagesDir + '''images/roast_dinner.jpg"),'''
        + '''(44, "Salmon and broccoli pasta", 4, "1. Set a large saucepan of water on the hob to boil and preheat the grill to medium-high. Arrange the salmon fillets on the grill rack and cook for 5 to 6 minutes. Turn off the grill and leave the salmon to rest.^^2. While the salmon is grilling, cook the pasta shapes in the boiling water for 8 minutes, then add the spring onions and broccoli and cook for a further 3 or 4 minutes.^^3. Put the peas in a large colander. Once the pasta, broccoli and spring onions are cooked, drain them into the colander over the peas ??? make sure to reserve 2 tablespoons of the cooking water in the pan.^^4. Put the soft cheese and skimmed milk into the hot saucepan with the reserved cooking water. Stir over a medium heat until smooth. Then add the lemon zest and chives.^^5. Return the pasta and vegetables to the saucepan with the sauce and heat gently for a couple of minutes, until warmed through.^^6. Carefully break the salmon into chunks and add to the pan ??? stir gently to avoid the salmon breaking up too much. Season everything with pepper, then serve each portion with 1 teaspoon of grated cheese on top.", "''' + programImagesDir + '''images/salmon__broccoli_pasta.jpg"),'''
        + '''(45, "Salmon with spring onion mash", 4, "1. Cook the potatoes in boiling water for 20 minutes, until tender, adding the spring onions to the saucepan 5 minutes before the end of cooking time.^^2. When the potatoes have been cooking for 10 minutes, start to prepare the salmon. Heat the vegetable oil oil in a non-stick frying pan, brushing it over the surface.^^3. Add the salmon, skin side down. Cook over a high heat for 2 to 3 minutes, without moving the fillets. Turn the salmon over, reduce the heat and cook for a further 3 to 4 minutes.^^4. At this point, put the broccoli on to cook in a little boiling water ??? it will take about 5 to 6 minutes. Let the salmon rest for a few minutes while making the mash.^^5. Drain the potatoes and spring onions and mash thoroughly. Beat in the milk and parsley. Reheat on the hob for 1 minute, beating well. Share the mash between 4 warmed plates and arrange the salmon fillets on top. Serve with the broccoli.", "''' + programImagesDir + '''images/salmon_with_spring_onion_mash.jpg"),'''
        + '''(46, "Sausage and bean stew", 4, "1. Preheat the grill to medium-high. Grill the sausages for 8 to 10 minutes, turning occasionally, until they're thoroughly cooked.^^2. While the sausages are cooking, heat the olive oil in a large saucepan and gently fry the onion and garlic for 2 or 3 minutes. Add the chopped tomatoes or passata, beans, potatoes and mixed herbs. Simmer for 15-20 minutes until the potatoes are tender.^^3. Slice the sausages and add them to the saucepan. Stir and cook for another 2 to 3 minutes to make sure they're warmed through. Serve in bowls and tuck in!", "''' + programImagesDir + '''images/sausage_bean_stew.jpg"),'''
        + '''(47, "Sausage, tomato and butter beans bake", 4, "1. Preheat the grill to medium, then grill the sausages for 1 to 2 minutes, or until just sealed and lightly browned on both sides. Transfer to a plate and set aside. Switch the oven to preheat to 200C (180C fan, gas mark 4).^^2. Gently heat the olive oil in a frying pan. Add the onion and sage, and fry over a low heat for about 10 minutes. The onion should be completely softened but not coloured.^^3. Turn the heat up to medium-low and add the tomatoes. Bring to a simmer, then cook for about 5 minutes, stirring now and then until the sauce is slightly reduced and thickened. Season with pepper.^^4. Transfer the tomato mixture to an oven dish and stir in the butter beans. Arrange the sausages evenly on top, and then push them down into the mixture.^^5. Cook in the oven for 15 to 20 minutes, until everything is bubbling, and the sausages are cooked through and tender. Serve straight to the table and let everyone tuck in.", "''' + programImagesDir + '''images/sausage_tomato_and_butter_bean_bake.jpg"),'''
        + '''(48, "Shakshuka", 4, "1. Heat the oil in a large non-stick frying pan on medium heat. Add the onion, peppers and garlic, and cook for about 5 minutes, stirring occasionally, until the vegetables soften.^^2. Stir in the aubergine and cook for another 5 minutes or so, until golden-brown. Add the tomatoes, tomato pur??e, salt, cumin and cayenne, and stir well. Bring to a boil, then lower the heat and cook for about 10 minutes, until the mixture thickens.^^3. Stir in the chickpeas, cover and cook for further 5 to 8 minutes on medium heat. Once the chickpeas have had time to soften, stir in the chopped spinach and lower the heat.^^4. Using a wooden spoon, create 6 wells in the mixture and crack 1 egg into each. Cover the pan and cook for about 6 to 8 minutes on low, until the egg whites set. If you prefer firmer yolks, cook for around 8 to 12 minutes.^^5. Once the eggs are cooked, take the mixture off the heat and leave to cool for a few minutes. Scatter with chopped coriander and serve.", "''' + programImagesDir + '''images/shakshuka.jpg"),'''
        + '''(49, "Super savoury rice", 4, "1. Heat the oil in a saucepan and fry the onion for 2 to 3 minutes, then add the mushrooms and cook for a further 2 minutes.^^2. Stir in the rice, then add the stock, peas, baby sweetcorn, tomatoes and curry powder. Stir well. Bring to the boil, turn down the heat and simmer for about 15 to 20 minutes, until the rice is tender, adding more water if necessary and then add a pinch of chilli flakes.^^3. Serve the rice in bowls and sprinkle the tomato on top.", "''' + programImagesDir + '''images/super_savoury_rice.jpg"),'''
        + '''(50, "Spaghetti bolognese", 4, "1. Heat a large saucepan and add the minced beef, a handful at a time, cooking until browned. Add the onion and cook for another few minutes.^^2. Add all the the remaining ingredients to the pan, apart from the spaghetti. Bring to the boil, then lower the heat and simmer gently for 15 to 20 minutes.^^3. When the sauce has been cooking for 10 minutes, start to cook the spaghetti. Bring a large saucepan of water to the boil, add the pasta and bring back to the boil. Stir well and cook for 8 to 10 minutes, until tender.^^4. Season the bolognese sauce with pepper. Drain the spaghetti and serve with the sauce.", "''' + programImagesDir + '''images/spaghetti_bolognese.jpg"),'''
        + '''(51, "Super stew and dumplings", 4, "1. Heat the vegetable oil in a large flameproof casserole dish or saucepan. Add the beef, a handful at a time, and cook over a high heat for about 2 to 3 minutes until sealed and browned.^^2. Pour the stock into the pan, then add the onions, garlic, carrots, celery, bay leaf and mushrooms. Bring to the boil, then reduce the heat. Cover and cook over a low heat for 90 minutes, checking the liquid level from time to time, and topping up with a little water if needed.^^3. To make the dumplings, sift the flour into a bowl and add the parsley and some black pepper. Add the reduced-fat spread to the flour, then rub in with your fingertips until the mixture looks like fine crumbs. Add just enough cold water (about 2 tablespoons) to make a soft dough. Knead the dough lightly for a moment, then form into 12 small dumplings.^^4. Add the dumplings to the stew, letting them sit on the surface. Cover and cook for another 25 to 30 minutes, until the dumplings are light and fluffy, then serve.", "''' + programImagesDir + '''images/super_stew_and_dumplings.jpg"),'''
        + '''(52, "Tasty veggie chilli", 4, "1. Heat the vegetable oil oil in a large saucepan and add the onion. Fry gently for 2 to 3 minutes, then add the carrot, garlic, red chilli and peppers and fry for 2 to 3 more minutes, stirring often.^^2. Add the frozen mince, beans, tomatoes, tomato pur??e and stock. Bring to the boil, then reduce the heat and simmer, partially covered, for 25 to 30 minutes. At the same time, put the rice on to cook in plenty of gently boiling water ??? it will take 25 to 30 minutes.^^3. Season the chilli with pepper, then serve in warm bowls with the cooked, drained rice.", "''' + programImagesDir + '''images/veggie_chilli.jpg"),'''
        + '''(53, "Tuna and bean jackets", 4, "1. Preheat the oven to 200C (fan 180C, gas mark 6). Prick the potatoes, then bake towards the top of the oven for 1 hour, or until tender.^^2. While the potatoes are cooking, mix together the cannellini beans, tuna, pepper, tomatoes, spring onions, vinegar and tomato pur??e. Season with black pepper.^^3. Split the baked potatoes open and fill them with the salsa mixture. Serve at once.", "''' + programImagesDir + '''images/tuna_and_bean_jackets.jpg"),'''
        + '''(54, "Turkey burgers", 4, "1. Preheat the grill to a medium-high heat. Put the turkey meat, onion, carrot, sweetcorn and herbs into a large bowl. Season with some pepper and mix together ??? you can do this with your hands if you like.^^2. Grill the burgers for 12 to 15 minutes, turning them over once, until browned and cooked through. Remove from the grill and let rest for a couple of minutes.^^3. While the cooked burgers are cooling, lightly toast the burger buns under the grill on the cut side only. Put some lettuce on the bottom halves and place the burgers on top. Add 2 slices of tomato onto each one and cover with the top half of the bun.", "''' + programImagesDir + '''images/turkey_burgers.jpg"),'''
        + '''(55, "Turkey koftas", 4, "1. Mix together the onion, carrot, mince, garlic, cumin, tomato pur??e, breadcrumbs and egg yolk.^^2. Divide the mixture into 8 pieces, then form a sausage shape with each piece and wrap around a skewer.^^3. Put the koftas in a foil-lined grill pan and put under a preheated grill for 15 to 20 minutes, turning occasionally.^^4. Meanwhile, prepare the dip by combining the yoghurt and mint. For the salad, layer the sliced tomatoes and onions, drizzle with the olive oil and sprinkle with black pepper.", "''' + programImagesDir + '''images/turkey_koftas.jpg"),'''
        + '''(56, "Turkey stir fry recipe", 4, "1. Put the noodles into a heatproof bowl and cover with boiling water. Soak for 6 minutes, or follow the instructions on the packet.^^2. Next, mix together the orange juice, soy sauce and cornflour until smooth. Set to one side. Heat the oil in a wok or very large frying pan.^^3. Add the turkey and stir-fry briskly for 3 to 4 minutes. Add the spring onions, pepper, carrot, celery and mushrooms. Stir-fry over a high heat for another 3 to 4 minutes, until the turkey is cooked. The vegetables should remain crisp and crunchy.^^4. Give the orange juice mixture a good stir, then add it to the stir-fry and cook for a few moments until thickened. Drain the noodles well, then add them to the turkey mixture. Serve at once.", "''' + programImagesDir + '''images/turkey_stir-fry.jpg"),'''
        + '''(57, "Veg and lentil cobbler", 4, "1. Preheat the oven to 180C (fan 160C, gas mark 4). Heat the olive oil in a large saucepan and cook the garlic and onion for 2 to 3 minutes. Add the celery, parsnip, carrots and cauliflower and stir-fry for 2 or 3 minutes more. Remove from the heat and add the mushrooms, tomatoes and lentils.^^2. Mix the cornflour with 3 to 4 tablespoons of water and add to the saucepan, along with the vegetable stock and parsley. Return to the heat and bring to the boil to thicken the mixture.^^3. Season with pepper then transfer the mixture to a casserole dish. Cover and bake in the oven for 20 minutes.^^4. Meanwhile, sift the flour into a large bowl and rub in the low-fat spread with your fingertips. Beat the egg and milk together in a separate bowl and add just enough to the dry mixture to make a soft dough. Knead lightly, then roll out on a lightly floured surface to a thickness of 2cm and cut into 4cm rounds. (When cutting out the rounds of dough, avoid twisting the cutter or the scones will not rise as much)^^5. Remove the casserole from the oven and turn the temperature up to 200C (fan 180C, gas mark 6). Arrange the scones around the edge of the dish and brush with the remaining egg and milk.^^6. Return to the oven uncovered and cook for a further 12 to 15 minutes, until the scone topping has risen and is golden brown.", "''' + programImagesDir + '''images/lentils_and_veg_cobbler.jpg"),'''
        + '''(58, "Vegetable frittata", 4, "1. Turn the grill on to preheat to a medium-high temperature.^^2. Heat the vegetable oil in a non-stick frying pan. Add the courgette and tomatoes and cook on the hob for 3 to 4 minutes, stirring often, until soft. Spread out over the base of the frying pan.^^3. Beat the eggs and milk together and pour into the frying pan. Cook over a medium-low heat for 4 or 5 minutes to set the base, then transfer to the grill to set the surface ??? about 3 minutes. Remove from the heat and let the frittata cool for 3 or 4 minutes.^^4. Toast the slices of bread. Slice the frittata into wedges and serve with the toast.", "''' + programImagesDir + '''images/veggie_frittata.jpg"),'''
        + '''(59, "Vegetable jalfrezi", 4, "1. Heat the vegetable oil in a large saucepan. Add the onions, apple and garlic and cook, stirring, for 3 to 4 minutes. Stir in the curry paste and cook for a few seconds.^^2. Add the carrot, pepper, tomatoes, cauliflower, chickpeas and stock. Simmer, partially covered, for 25 to 30 minutes, adding a little extra stock or water if needed. At the same time, cook the rice in a large saucepan of gently boiling water. It will take about 30 minutes.^^3. Add the peas and coriander to the curry and heat for 2 to 3 minutes. Check the seasoning, adding a little ground black pepper if needed.^^4. Serve the vegetable curry on warmed plates, with the rice, topping each portion with 1 tablespoon of low-fat yoghurt.", "''' + programImagesDir + '''images/vegetable_jalfrezi.jpg"),'''
        + '''(60, "Zombie peppers", 4, "1. Slice the tops off the peppers and put the lids aside. Remove and throw away the seeds. With a sharp knife, carefully carve a spooky face into each pepper. Once they're scary enough, put the peppers in a roasting tray and turn on the oven to preheat to 180C (fan 160C, gas mark 4).^^2. Bring a pan of water to the boil and cook the rice according to the packet instructions. When it's ready, drain and set aside.^^3. While the rice is cooking, heat the oil in a saucepan over a medium-high heat and fry the onions until softened and beginning to go see-through ??? about 5 minutes.^^4. Take the pan off the heat, then add in the cooked rice, grated beetroot, grated cheese, Worcestershire sauce, black pepper and herbs. Mix well.^^5. Spoon the filling into the peppers, and put their lids back on. Roast in the oven for 45 minutes, or until they've softened but are still holding their scary shape! Leave to cool for 5 minutes, then dish up with a side of salad and enjoy.", "''' + programImagesDir + '''images/zombie_peppers.jpg"),'''
        + '''(61, "Baked tomatoes on toast", 4, "1. Preheat the oven to 190C (fan oven 170C, gas mark 5).^^2. Arrange the tomatoes, cut sides up, on a baking sheet. Sprinkle with the dried herbs and chives (if using) and season with black pepper. Bake for 10 minutes.^^3. Sprinkle the breadcrumbs and cheese over the tomatoes, and bake for another 5 minutes.^^4. Meanwhile, toast the bread. Place the toast on warmed plates and share the tomatoes between them. Sprinkle with a little extra black pepper, then serve.", "''' + programImagesDir + '''images/baked_tomatos_on_toast.jpg"),'''
        + '''(62, "Beefed up sarnies", 4, "1. In a bowl, mix together the carrot, beetroot and red onion with the vinegar. Season with black pepper.^^2. Spread each slice of bread with 1 teaspoon of mayonnaise, then top 4 of them with the lettuce leaves and the roast beef. Share the salad between them, then sandwich together with the remaining slices of bread.^^3. Cut in half and serve at once, or wrap and keep cool to serve later.", "''' + programImagesDir + '''images/beefed_up_sarnies.jpg");''')

    cursor.execute(create_meals_table_query)
    print(insert_meals_query)
    cursor.execute(insert_meals_query)


def mealPlanFunc(cursor):       #This function is responsible for creating the meal_plan table
    create_meal_plan_query = """
        CREATE TABLE meal_plan(
            meal_date DATE, meal_id INT, amount INT, FOREIGN KEY(meal_id) REFERENCES meals(id), PRIMARY KEY (meal_date, meal_id)
        );
        """

    cursor.execute(create_meal_plan_query)

def mealIngredientsFunc(cursor):
    create_meal_ingredients_query = """
        CREATE TABLE meal_ingredients(
            meal_id INT, ingredient_id INT, grams_amount FLOAT, FOREIGN KEY (ingredient_id) REFERENCES ingredients(id), FOREIGN KEY (meal_id) REFERENCES meals(id), PRIMARY KEY (meal_id, ingredient_id)
        );
    """

    insert_meal_ingredients_query = """
        INSERT INTO meal_ingredients(meal_id, ingredient_id, grams_amount)
        VALUES
            (1, 2, 8.4),
            (1, 1, 500),
            (1, 3, 285),
            (1, 4, 130),
            (1, 5, 20),
            (1, 6, 14.3),
            (1, 7, 448),
            (1, 8, 25),
            (1, 10, 25),
            (1, 11, 300),
            (1, 12, 14.3),
            (1, 14, 150),
            (1, 16, 57.2),
            (1, 17, 14.3),
            (1, 18, 0.26),
            (2, 19, 30),
            (2, 1, 700),
            (2, 3, 510),
            (2, 20, 148),
            (2, 21, 148),
            (2, 23, 100),
            (2, 5, 40),
            (2, 24, 20),
            (2, 25, 400),
            (2, 120, 4.2),
            (2, 27, 4.2),
            (2, 28, 6.3),
            (2, 29, 4.2),
            (2, 30, 4.2),
            (2, 31, 6.3),
            (2, 32, 250),
            (3, 33, 240),
            (3, 3, 340),
            (3, 20, 148),
            (3, 34, 156),
            (3, 5, 20),
            (3, 35, 8.4),
            (3, 25, 800),
            (3, 36, 28.6),
            (3, 37, 28.6),
            (3, 38, 200),
            (4, 2, 8.4),
            (4, 3, 150),
            (4, 5, 50),
            (4, 39, 4.2),
            (4, 28, 4.2),
            (4, 40, 120),
            (4, 41, 600),
            (4, 27, 4.2),
            (4, 35, 4.2),
            (4, 31, 8.4),
            (4, 7,448),
            (4, 34, 100),
            (4, 38, 200),
            (4, 32, 600),
            (5, 38, 150),
            (5, 43, 227),
            (5, 12, 14.3),
            (5, 37, 28.6),
            (5, 44, 4.2),
            (5, 2, 8.4),
            (5, 1, 300),
            (5, 3, 170),
            (5, 20, 148),
            (5, 45, 120),
            (5, 40, 246),
            (5, 18, 0.26),          
            (6, 17,   60),
            (6, 50,   35),
            (6, 45,   100),
            (6, 46,   45),
            (6, 5,   30),
            (6, 53,   80),
            (6, 54,   8.4),
            (6, 56,   650),
            (6, 2,   18.5),
            (6, 21,   60),
            (6, 20,   60),
            (6, 52,   3.9),
            (6, 25,   400),
            (6, 60,   10),
            (6, 120,   2.1),
            (6, 58,   200),
            (6, 59,   100),
            (6, 32,   600),
            (7, 37,   8.4),
            (7, 44,   8.4),
            (7, 61,   28.6),
            (7, 63,   352),
            (7, 64,   880),
            (7, 34,   320),
            (7, 65,   320),
            (7, 66,   57.2),
            (7, 18,   0.36),
            (8, 67,   1000),
            (8, 59,   72),
            (8, 68,   180),
            (8, 23,   80),
            (8, 69,   75),
            (8, 70,   28.6),
            (8, 71,   57.2),
            (8, 2,   21.45),
            (8, 72,   4.2),
            (8, 120,   2.1),
            (8, 73,   4.2),
            (8, 53,   60),
            (8, 27,   2.1),
            (8, 42,   2.1),
            (8, 31,   2.1),
            (8, 17,   10),
            (9, 74,   125),
            (9, 52,   1.3),
            (9, 18,   4.2),
            (9, 75,   4.2),
            (9, 5,   6),
            (9, 76,   100),
            (9, 38,   125),
            (9, 77,   300),
            (9, 2,   12.6),
            (9, 3,   220),
            (9, 72,   24),
            (9, 27,   2.1),
            (9, 78,   4.2),
            (9, 79,   8.4),
            (9, 60,   15),
            (9, 80,   4.2),
            (9, 81,   224),
            (9, 82,   0.2),
            (9, 83,   125),
            (9, 46,   75),
            (9, 17,   28.6),
            (10, 90,   10),
            (10, 84,   120),
            (10, 40,   100),
            (10, 85,   80),
            (10, 20,   120),
            (10, 21,   120),
            (10, 86,   150),
            (10, 87,   40),
            (10, 88,   72),
            (10, 51,   100),
            (10, 89,   12.6),
            (10, 18,   0.36),
            (11, 2,   2.1),
            (11, 91,   560),
            (11, 37,   57.2),
            (11, 40,   400),
            (11, 18,   0.36),
            (11, 85,   40),
            (12, 40,   400),
            (12, 92,   750),
            (12, 93,   180),
            (12, 94,   35),
            (12, 95,   20),
            (12, 66,   300),
            (12, 85,   75),
            (12, 96,   4.2),
            (12, 18,   0.36),
            (13, 1,   600),
            (13, 46,   60),
            (13, 34,   72),
            (13, 47,   200),
            (13, 48,   4.2),
            (13, 49,   4.2),
            (13, 44,   8.4),
            (13, 18,   0.36),
            (14, 3,   80),
            (14, 74,   210),
            (14, 98,   38),
            (14, 29,   8.4),
            (14, 99,   50),
            (14, 37,   14.3),
            (14, 103,   120),
            (14, 100,   110),
            (14, 101,   40),
            (14, 102,   272),
            (15, 97,   300),
            (15, 3,   150),
            (15, 5,   12),
            (15, 40,   400),
            (15, 37,   28.6),
            (15, 29,   8.4),
            (15, 42,   4.2),
            (15, 20,   120),
            (15, 86,   200),
            (15, 74,   410),
            (15, 7,   150),
            (15, 38,   300),
            (15, 18,   0.36),
            (16, 64,   1000),
            (16, 97,   350),
            (16, 3,   80),
            (16, 34,   72),
            (16, 47,   200),
            (16, 104,   100),
            (16, 105,   4.2),
            (16, 18,   0.36),
            (16, 32,   450),
            (16, 106,   16.8),
            (16, 107,   50),
            (17, 108,   180),
            (17, 109,   6.3),
            (17, 110,   2.1),
            (17, 99,   200),
            (17, 66,   250),
            (17, 46,   30),
            (17, 107,   350),
            (17, 113,   130),
            (17, 35,   4.2),
            (17, 2,   14.3),
            (17, 53,   10),
            (17, 17,   10),
            (17, 111,   250),
            (17, 112,   10),
            (17, 18,   0.72),
            (18, 2,   28.6),
            (18, 28,   3.2),
            (18, 114,   3.2),
            (18, 115,   3.2),
            (18, 116,   3.2),
            (18, 117,   1.4),
            (18, 82,   0.4),
            (18, 3,   110),
            (18, 5,   24),
            (18, 24,   14.3),
            (18, 64,   510),
            (18, 59,   450),
            (18, 32,   350),
            (19, 118,   300),
            (19, 3,   150),
            (19, 2,   8.4),
            (19, 29,   4.2),
            (19, 120,   4.2),
            (19, 20,   150),
            (19, 32,   1000),
            (19, 119,   480),
            (20, 83,   700),
            (20, 66,   425),
            (20, 95,   25),
            (20, 94,   25),
            (20, 50,   28.6),
            (20, 65,   100),
            (20, 18,   0.36),
            (20, 57,   300),
            (20, 85,   25),
            (21, 121,   145),
            (21, 37,   1),
            (21, 40,   200),
            (21, 122,   50),
            (21, 89,   4.2),
            (21, 93,   25),
            (21, 43,   25),
            (21, 86,   20),
            (21, 1,   25),
            (22, 68,   680),
            (22, 2,   14.3),
            (22, 123,   75),
            (22, 99,   50),
            (22, 32,   28.6),
            (22, 91,   560),
            (22, 124,   300),
            (22, 18,   0.36),
            (23, 5,   6),
            (23, 61,   21.4),
            (23, 137,   14.3),
            (23, 138,   8.4),
            (23, 1,   300),
            (23, 20,   120),
            (23, 3,   110),
            (24, 38,   300),
            (24, 99,   200),
            (24, 56,   200),
            (24, 140,   120),
            (24, 141,   120),
            (24, 35,   8.4),
            (24, 65,   150),
            (24, 50,   28.6),
            (24, 18,   0.36),
            (25, 142,   100),
            (25, 2,   4.2),
            (25, 21,   120),
            (25, 47,   160),
            (25, 65,   100),
            (25, 99,   200),
            (25, 66,   8.4),
            (25, 85,   50),
            (25, 130,   8.4),
            (25, 18,   0.36),
            (25, 87,   200),
            (26, 142,   300),
            (26, 95,   40),
            (26, 3,   80),
            (26, 94,   50),
            (26, 66,   600),
            (26, 85,   75),
            (26, 143,   4.2),
            (26, 18,   0.36),
            (26, 40,   250),
            (27, 56,   560),
            (27, 27,   2.1),
            (27, 120,   2.1),
            (27, 40,   400),
            (27, 5,   18),
            (27, 144,   80),
            (27, 145,   14.3),
            (27, 116,   4.2),
            (27, 32,   470),
            (27, 146,   57.2),
            (27, 17,   20),
            (28, 142,   400),
            (28, 147,   800),
            (28, 95,   14.3),
            (28, 94,   14.3),
            (28, 66,   500),
            (28, 143,   4.2),
            (28, 148,   100),
            (28, 65,   150),
            (28, 85,   100),
            (28, 42,   2.1),
            (28, 18,   4.2),
            (28, 123,   100),
            (29, 64,   600),
            (29, 149,   500),
            (29, 2,   4.2),
            (29, 3,   110),
            (29, 5,   12),
            (29, 34,   144),
            (29, 150,   300),
            (29, 40,   400),
            (29, 81,   150),
            (29, 35,   8.4),
            (29, 86,   100),
            (29, 47,   200),
            (29, 18,   0.36),
            (29, 12,   28.6),
            (30, 3,   110),
            (30, 5,   12),
            (30, 97,   200),
            (30, 137,   14.3),
            (30, 25,   400),
            (30, 151,   200),
            (30, 86,   200),
            (30, 21,   120),
            (30, 130,   8.4),
            (30, 37,   8.4),
            (31, 68,   800),
            (31, 152,   50),
            (31, 137,   4.2),
            (31, 47,   200),
            (31, 67,   270),
            (31, 21,   120),
            (31, 20,   120),
            (31, 153,   14.3),
            (32, 2,   4.2),
            (32, 46,   75),
            (32, 154,   300),
            (32, 5,   6),
            (32, 86,   60),
            (32, 81,   900),
            (32, 65,   75),
            (32, 18,   0.36),
            (33, 34,   300),
            (33, 155,   300),
            (33, 64,   700),
            (33, 156,   536),
            (33, 2,   4.2),
            (33, 100,   150),
            (33, 7,   100),
            (33, 50,   14.3),
            (33, 105,   4.2),
            (33, 12,   28.6),
            (33, 32,   214.3),
            (33, 18,   0.36),
            (34, 157,   1500),
            (34, 19,   30),
            (34, 3,   150),
            (34, 120,   4.2),
            (34, 5,   36),
            (34, 40,   200),
            (34, 144,   50),
            (34, 27,   2.1),
            (34, 42,   4.2),
            (34, 64,   800),
            (35, 158,   50),
            (35, 159,   170),
            (35, 32,   1500),
            (35, 3,   150),
            (35, 5,   24),
            (35, 144,   40),
            (35, 19,   30),
            (35, 120,   4.2),
            (35, 27,   6.3),
            (35, 28,   4.2),
            (35, 17,   20),
            (36, 19,   30),
            (36, 3,   220),
            (36, 5,   24),
            (36, 25,   400),
            (36, 24,   20),
            (36, 144,   40),
            (36, 65,   150),
            (36, 27,   6.3),
            (36, 26,   700),
            (36, 120,   4.2),
            (36, 42,   6.3),
            (36, 31,   6.3),
            (36, 30,   8.4),
            (36, 17,   20),
            (37, 160,   300),
            (37, 161,   120),
            (37, 46,   75),
            (37, 162,   150),
            (37, 99,   50),
            (37, 66,   150),
            (37, 85,   40),
            (37, 2,   4.2),
            (37, 50,   28.6),
            (37, 18,   0.36),
            (38, 142,   200),
            (38, 137,   14.3),
            (38, 3,   220),
            (38, 5,   6),
            (38, 129,   4.2),
            (38, 40,   400),
            (38, 47,   800),
            (38, 7,   125),
            (38, 85,   25),
            (38, 18,   0.36),
            (39, 2,   14.3),
            (39, 3,   220),
            (39, 5,   6),
            (39, 154,   300),
            (39, 81,   1200),
            (39, 65,   500),
            (39, 148,   80),
            (39, 164,   125),
            (39, 112,   10),
            (39, 85,   50),
            (40, 21,   240),
            (40, 22,   120),
            (40, 20,   120),
            (40, 38,   150),
            (40, 2,   4.2),
            (40, 3,   110),
            (40, 5,   6),
            (40, 165,   300),
            (40, 40,   200),
            (40, 65,   75),
            (40, 78,   4.2),
            (40, 105,   4.2),
            (40, 18,   0.36),
            (41, 137,   4.2),
            (41, 3,   80),
            (41, 5,   6),
            (41, 40,   400),
            (41, 37,   28.6),
            (41, 105,   8.4),
            (41, 18,   0.36),
            (41, 151,   350),
            (41, 90,   14.3),
            (42, 166,   680),
            (42, 2,   4.2),
            (42, 3,   80),
            (42, 20,   120),
            (42, 21,   120),
            (42, 78,   12.6),
            (42, 129,   8.4),
            (42, 94,   30),
            (42, 18,   0.36),
            (42, 1,   600),
            (42, 7,   300),
            (42, 147,   500),
            (43, 167,   2000),
            (43, 64,   1200),
            (43, 2,   4.2),
            (43, 34,   288),
            (43, 92,   250),
            (43, 168,   350),
            (43, 65,   150),
            (43, 106,   16.8),
            (44, 141,   240),
            (44, 151,   250),
            (44, 46,   75),
            (44, 147,   400),
            (44, 65,   100),
            (44, 170,   150),
            (44, 66,   150),
            (44, 171,   2),
            (44, 172,   28.6),
            (44, 18,   0.36),
            (44, 169,   16.8),
            (45, 64,   1000),
            (45, 46,   90),
            (45, 2,   4.2),
            (45, 141,   480),
            (45, 66,   57.2),
            (45, 50,   28.6),
            (45, 147,   250),
            (45, 18,   0.36),
            (46, 156,   134),
            (46, 2,   8.4),
            (46, 3,   150),
            (46, 5,   12),
            (46, 25,   400),
            (46, 173,   410),
            (46, 64,   100),
            (46, 105,   8.4),
            (46, 18,   0.36),
            (47, 156,   536),
            (47, 137,   8.4),
            (47, 3,   150),
            (47, 174,   14.3),
            (47, 25,   400),
            (47, 173,   800),
            (47, 18,   0.36),
            (48, 2,   14.3),
            (48, 3,   110),
            (48, 20,   60),
            (48, 21,   60),
            (48, 5,   36),
            (48, 67,   270),
            (48, 25,   800),
            (48, 37,   28.6),
            (48, 42,   8.4),
            (48, 175,   400),
            (48, 120,   2.1),
            (48, 133,   2.1),
            (48, 148,   200),
            (48, 99,   300),
            (48, 17,   15),
            (49, 2,   4.2),
            (49, 3,   110),
            (49, 86,   100),
            (49, 38,   150),
            (49, 7,   300),
            (49, 65,   75),
            (49, 176,   100),
            (49, 29,   0.36),
            (49, 35,   4.2),
            (50, 97,   300),
            (50, 40,   400),
            (50, 160,   300),
            (50, 3,   150),
            (50, 5,   12),
            (50, 37,   28.6),
            (50, 105,   8.4),
            (50, 20,   120),
            (50, 86,   40),
            (50, 34,   72),
            (50, 47,   200),
            (50, 7,   150),
            (50, 18,   0.36),
            (51, 2,   8.4),
            (51, 177,   280),
            (51, 81,   450),
            (51, 3,   220),
            (51, 5,   12),
            (51, 34,   144),
            (51, 45,   100),
            (51, 82,   0.2),
            (51, 86,   250),
            (51, 178,   100),
            (51, 50,   28.6),
            (51, 95,   50),
            (51, 18,   0.36),
            (52, 2,   8.4),
            (52, 5,   12),
            (52, 53,   20),
            (52, 150,   300),
            (52, 74,   420),
            (52, 38,   200),
            (52, 3,   110),
            (52, 34,   72),
            (52, 20,   120),
            (52, 21,   120),
            (52, 37,   8.4),
            (52, 81,   100),
            (52, 18,   0.36),
            (53, 166,   680),
            (53, 173,   400),
            (53, 179,   200),
            (53, 37,   8.4),
            (53, 20,   120),
            (53, 103,   200),
            (53, 46,   60),
            (53, 18,   0.36),
            (54, 26,   450),
            (54, 3,   80),
            (54, 34,   72),
            (54, 107,   50),
            (54, 105,   8.4),
            (54, 18,   0.36),
            (54, 180,   380),
            (54, 101,   20),
            (54, 103,   200),
            (55, 3,   55),
            (55, 34,   50),
            (55, 26,   250),
            (55, 5,   6),
            (55, 42,   4.2),
            (55, 37,   14.3),
            (55, 123,   38),
            (55, 181,   18),
            (55, 111,   57.2),
            (55, 112,   28.6),
            (55, 103,   200),
            (55, 100,   110),
            (55, 137,   8.4),
            (55, 18,   0.36),
            (56, 182,   125),
            (56, 184,   57.2),
            (56, 44,   14.3),
            (56, 12,   14.3),
            (56, 2,   14.3),
            (56, 165,   350),
            (56, 46,   75),
            (56, 21,   120),
            (56, 34,   72),
            (56, 45,   100),
            (56, 86,   20),
            (56, 18,   0.36),
            (57, 137,   8.4),
            (57, 5,   6),
            (57, 3,   110),
            (57, 45,   100),
            (57, 185,   150),
            (57, 34,   144),
            (57, 186,   420),
            (57, 86,   50),
            (57, 25,   400),
            (57, 187,   75),
            (57, 12,   28.6),
            (57, 81,   450),
            (57, 50,   4.2),
            (57, 18,   0.36),
            (57, 178,   150),
            (57, 95,   45),
            (57, 99,   50),
            (57, 66,   30),
            (58, 2,   8.4),
            (58, 99,   300),
            (58, 66,   28.6),
            (58, 98,   152),
            (58, 40,   200),
            (58, 47,   200),
            (58, 18,   0.36),
            (59, 2,   8.4),
            (59, 3,   220),
            (59, 136,   100),
            (59, 5,   6),
            (59, 188,   28.6),
            (59, 34,   72),
            (59, 22,   120),
            (59, 40,   400),
            (59, 186,   120),
            (59, 175,   410),
            (59, 81,   300),
            (59, 189,   180),
            (59, 65,   50),
            (59, 17,   28.6),
            (59, 16,   57.2),
            (59, 18,   0.36),
            (60, 21,   240),
            (60, 22,   120),
            (60, 20,   120),
            (60, 38,   200),
            (60, 2,   14.3),
            (60, 3,   220),
            (60, 190,   150),
            (60, 191,   14.3),
            (60, 122,   50),
            (60, 85,   50),
            (60, 105,   8.4),
            (60, 18,   0.36),
            (61, 40,   800),
            (61, 192,   300),
            (61, 105,   4.2),
            (61, 172,   8.4),
            (61, 123,   28.6),
            (61, 169,   16.8),
            (61, 98,   152),
            (61, 18,   0.36),
            (62, 88,   72),
            (62, 190,   110),
            (62, 100,   40),
            (62, 193,   8.4),
            (62, 98,   304),
            (62, 194,   33.6),
            (62, 87,   24),
            (62, 195,   100),
            (62, 18,   0.36);
        """

    cursor.execute(create_meal_ingredients_query)
    cursor.execute(insert_meal_ingredients_query)

def mealNutritionFunc(cursor):
    create_meal_nutrition_query = """
        CREATE TABLE meal_nutrition(
            meal_id INT,
            energy FLOAT,
            fat FLOAT,
            sat_fat FLOAT,
            carbs FLOAT,
            sugar FLOAT,
            fibre FLOAT,
            protein FLOAT,
            salt FLOAT,
            vit_a FLOAT,
            thiamin FLOAT,
            riboflavin FLOAT,
            niacin FLOAT,
            vit_b6 FLOAT,
            vit_b12 FLOAT,
            vit_c FLOAT,
            vit_d FLOAT,
            calcium FLOAT,
            phosphorus FLOAT,
            magnesium FLOAT,
            potassium FLOAT,
            iron FLOAT,
            zinc FLOAT,
            copper FLOAT,
            selenium FLOAT,
            FOREIGN KEY (meal_id) REFERENCES meals(id), PRIMARY KEY (meal_id)
        );
    """

    cursor.execute(create_meal_nutrition_query)
    

def createAllTablesFunc():
    if checkTablesFunc(cursor, "ingredients") == False:
        ingredientsTableFunc(cursor)

    if checkTablesFunc(cursor, "meals") == False:
        mealsTableFunc(cursor)

    if checkTablesFunc(cursor, "meal_ingredients") == False:
        mealIngredientsFunc(cursor)

    if checkTablesFunc(cursor, "meal_nutrition") == False:
        mealNutritionFunc(cursor)

    if checkTablesFunc(cursor, "meal_plan") == False:
        mealPlanFunc(cursor)

def deleteAllTablesFunc(cursor):
    table_array = ["meal_plan", "meal_nutrition", "meal_ingredients", "meals", "ingredients"]

    for i in range (0, len(table_array)):
        cursor.execute("DROP TABLE " + str(table_array[i]))


try:
    checkMealDBFunc() #Calls the functiont that checks if the meal_db database exists and if it doesn't then it creates it
    mealDBConnect = connect(host="localhost", user = dbUser, password = dbPasswd, database="meal_db")  #Creates a connection to the meal_db database
    with mealDBConnect as connection:
        show_db_query = "SHOW DATABASES;"
        
        show_table_query = "DESCRIBE ingredients"
        
        select_ingredients_query = "SELECT * FROM ingredients"
        select_meals_query = "SELECT * FROM meals"
        select_chicken_banana_korma_query = "SELECT * FROM chicken_and_banana_korma"
        delete_ingredient = "DELETE FROM ingredients WHERE id=2"
        select_meal_image = "SELECT img_dir FROM meals"

        check_table_query = """
        SELECT * FROM information_schema.TABLES
        WHERE
            TABLE_SCHEMA LIKE "meal_db" AND
            TABLE_TYPE LIKE "BASE TABLE" AND
            TABLE_NAME = "meals"
        """
        
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)

            createAllTablesFunc()   #Run this function to create the database, create the tables and to populate all the tables with the default values
            #deleteAllTablesFunc(cursor)    #Run this function to delete all of the tables from the database
            
            #cursor.execute(delete_ingredient)
            connection.commit()
            
            #cursor.execute(show_table_query)
            # Fetch rows from last executed query
            result = cursor.fetchall()
            for row in result:
                print(row)

            print("")
            print("")
            print("")

            print("Ingredients table")
            cursor.execute(select_ingredients_query) 
            result = cursor.fetchall()
            for row in result:
                print(row)

            print("")
            print("Meals table")
            cursor.execute(select_meals_query)
            result = cursor.fetchall()
            for row in result:
                print(row)

            meal_images_array = [] 

            print("")
            print("All meal images")
            cursor.execute(select_meal_image)
            result = cursor.fetchall()
            for row in result:
                temp = str(row)
                temp = temp[2:]
                temp = temp[:-3]
                meal_images_array.append(temp)

            print(meal_images_array)
            
except Error as e:
    print(e)
