from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
import tkinter.font as font
from PIL import ImageTk, Image
from mysql.connector import connect, Error
from datetime import date, datetime
from tkcalendar import *
import math
from tkinter import filedialog
from os.path import exists

root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.state("zoomed")

dbUser = "MYSQL_USERNAME"        #MySQL username
dbPasswd = "MYSQL_PASSWORD"   #MySQL password
programImagesDir = "C:/Users/PC/Desktop/meal_program/"  #This variable id used to store the direcotry that the image folder is in


#Load data from the database for page 1

mealImagesArray = []
mealNameArray = []

mealClicked = None          #This global vairable is used to store the path name of the meal button that has been
                            #click on the meals page so that it can be deleted if a users chooses to delete it
newMealWinOpen = False      #This global variable is used to tell if the new meal window is already open
addMealCurrentRoot = None   #This variable is used to keep a reference to the new meal window so that if it
                            #already exists then it can be brough to the front 

def readDBQuery(queryString):       #This function is used to read from the database
    try:
        mydb = connect(host="localhost", user = dbUser, password = dbPasswd, database="meal_db")
        with mydb as connection:
            with connection.cursor() as cursor:
                cursor.execute(queryString)
                result = cursor.fetchall()
        mydb.close()        #Closes the connection
    except Error as e:
        print(e)
    return result

def writeDBQuery(queryString):      #This functions is used to write to the database
    try:
        mydb = connect(host="localhost", user = dbUser, password = dbPasswd, database="meal_db")
        with mydb as connection:
            with connection.cursor() as cursor:
                cursor.execute(queryString)
                result = cursor.fetchall()

                connection.commit()

        mydb.close()        #Closes the connection
    except Error as e:
        print(e)

def loadDataMealPgFunc():      #This function reads in all of the image directories for all of the meals in the meals table
    result = readDBQuery("SELECT img_dir FROM meals")
    for row in result:  #This for loop reads each image directory in result and stores it in the mealImagesArray
        mealImagesArray.append(row[0])

    result = readDBQuery("SELECT name FROM meals")
    for row in result:  #This for loop reads each meal name in result and stores it in the mealNameArray
        mealNameArray.append(row[0])

def readMealFromDBFunc(meal_id):    #This function is used to read all of the information that is
                                    #needed about the specifed meal from the database
    mealDetails = []
    mealIngredients = []

    mealIngredientsNameArray = []       #Used to temporarly store all the ingredient names read from the database
    mealIngredientsGramsArray = []      #Used to temporarly store all the gram amounts read from the database
    mealIngredientsIsLiquidArray = []   #Used to temporarly store if the ingredient is a liquid 
    ingredients_text = ""               #Used to store all the instructions in a single string with the instructions in the
                                        #format grams + unit + ingredient name
    instructions_text = ""              #Used to store the instructions for the meal
    num_servings_text = ""              #Used to store the number of serving for the meal
    meal_name_text = ""                #Used to store the name of the meal
    img_dir_text = ""                   #Used to store the directory for the meals image


    #Used to read the name, number of servings, instructions and image directory
    mealTableValues = readDBQuery('SELECT name, num_servings, instructions, img_dir FROM meals WHERE id = ' + str(meal_id) + ';')

    meal_name_text = str(mealTableValues[0][0])
    num_servings_text = str(mealTableValues[0][1])
    instructions_text = str(mealTableValues[0][2])
    img_dir_text = str(mealTableValues[0][3])
                                        
    result = readDBQuery("SELECT ingredient_id, grams_amount FROM meal_ingredients WHERE meal_id = " + str(meal_id))
    for row in result:  #This for loop converts the result to a string, removes the (' from the start of the text and ',)
                        #from the end of the text and then stores it in the mealIngredients array
        temp = str(row[0]) + ", " + (str(row[1]).replace(".0", ""))
        mealIngredients.append(temp)        #Adds the ingredient id and grams amount to the array e.g. 1, 500, the id of the
                                            #ingredient is need so that the name can be read from the database


            
    for i in range(0, len(mealIngredients)):
        tempArray = mealIngredients[i].split(",")       #Used to seperate the ingredients id from its grams amount
        mealIngredientsGramsArray.append(str(tempArray[1]))     #Adds the ingredients gram amount to the array
                    
        result = readDBQuery("SELECT name, is_liquid FROM ingredients WHERE id = " + str(tempArray[0]) )
        for row in result:
            mealIngredientsNameArray.append(str(row[0]))    #Adds the ingredients name to the array
            mealIngredientsIsLiquidArray.append(str(row[1]))    #Add the ingredients liquid status to the arrya 0 for
                                                                #not liquid 1 for is liquid


    for x in range(0, len(mealIngredientsNameArray)):
        unit = ""
        amount = (mealIngredientsGramsArray[x]).strip()     #Stores the grams amount as text with any white space removed
        name= ((mealIngredientsNameArray[x].split("("))[0]).strip()     #Stored the ingredients name with any end bracket
                                                                        #information remove e.g. (USDA) and any
                                                                        #white space removed

        if str(mealIngredientsIsLiquidArray[x]) == "0": #Used to decided the units that should be used for the ingredient
            unit = "g"
        elif str(mealIngredientsIsLiquidArray[x]) == "1":
            unit = "ml"
                    
                        
        if x != len(mealIngredientsNameArray):      #Used to put each ingredient on a seprate line without having an
                                                    #additional blank line on the last ingredient
            ingredients_text = ingredients_text + (str(name) + " " + str(amount) + str(unit) + "\n")
        else:
            ingredients_text = ingredients_text + (str(name) + " " + str(amount) + str(unit))


    return ingredients_text, instructions_text, num_servings_text, meal_name_text, img_dir_text

def manageCharacterLengthFunc(length, instruction_str):
    output_string = ""
    paragraphArray = instruction_str.split("^")       #Used to split the text where there a break lines in the text


    for n in range (0, len(paragraphArray)):
        tempStr = paragraphArray[n]     #Used to put each number paragraph into its own element within the array
        stringArray = tempStr.split(" ")   #Splits the string up so that each word is in its own element within the array

        if n != 0:
            output_string = output_string + "\n"      #Used so that there is a line space for every breakline that was in the text
     
        total_chars = 0     #This variable is used to store the current amount of characters on a line

        for i in range(0, len(stringArray)):
            total_chars = total_chars + len(stringArray[i])     #Adds the length of the word that is about to be
                                                                #added to the total_chars variable

            if total_chars < length:    #This is true if the total amount of characters is less than the set limit
                output_string = output_string + str(stringArray[i]) + " "   #Adds the word to the string with a space add to the
                                                                            #end so that there is a space between the words
                total_chars = total_chars + 1       #Increases the total_chars variable by an additional 1
                                                    #to account for the space that was added
            else:
                output_string = output_string + "\n" + str(stringArray[i]) + " "    #Run when the  total_chars is larger than the
                                                                                    #set limit, as a result a break line is added
                                                                                    #so the word is dislay on the line below
                total_chars = len(stringArray[i])   #Sets the total_chars variable to the length of the word that was
                                                    #just added so that the new line is able to take into account the
                                                    #new word that has just been added

            if i == (len(stringArray) - 1):     #Sets total_chars back to zero when the for loop has reached the end of the
                                                #paragraph, so that the next paragraph isn't effected by the previous one
                total_chars = 0

    return output_string


loadDataMealPgFunc()

#Setup the main frame, canvas, scrollbar and child frames ------------------------------------------------------------------------

#Create a main frame
mainFrame = Frame(root)
mainFrame.grid(row=0, column=0, sticky="nesw")
mainFrame.rowconfigure(index=0, weight=1)       #Set the row and column weight so that the frames
                                                #that are added scale to the whole window
mainFrame.columnconfigure(index=0, weight=1)

#Creates a canvas
myCanvas = Canvas(mainFrame, highlightthickness=0)      #Highlight thickness is set to 0 so that a border doesn't
                                                        #appear when a user click into an entry box
myCanvas.grid(row=0, column=0, sticky="nesw")

#Adds a scrollbar to the canvas
myScrollbar = Scrollbar(mainFrame, orient=VERTICAL, command=myCanvas.yview)     #Orient the scrollbar vertically and assign
                                                                                #it to scroll in the y axis
myScrollbar.grid(row=0, column=1, sticky="ns")  #Places the scrollbar in column 1 as the canvas is in column 0

#Configure the canvas
myCanvas.configure(yscrollcommand=myScrollbar.set)      #Links the canvas with the scrollbar
#Set the Bbox so the scroll bar knows the scroll region when the scroll bar is first added to the canvas
myCanvas.bind("<Configure>", lambda e: myCanvas.configure(scrollregion = myCanvas.bbox("all")))     

#Create the frames for inside the canvas
canvasParentFrame = Frame(myCanvas)
menuFrame = Frame(canvasParentFrame)
childFrame1 = Frame(canvasParentFrame)  #Used as the frame for the Calendar page
childFrame2 = Frame(canvasParentFrame)  #Used as the frame for the Meals page
childFrame3 = Frame(canvasParentFrame)  #Used as the frame for the analytics page
childFrame4 = Frame(canvasParentFrame)  #Used as the frame for the individual meal pages
childFrame5 = Frame(canvasParentFrame)  #Used as the frame for the info about a date on the calendar page

childFrameArray = [childFrame1, childFrame2, childFrame3, childFrame4, childFrame5]     #This array is used for controlling
                                                                                        #which childFrame is visible

menuFrame.grid(row=0, column=0, sticky="nesw")  #Places the menuFrame in row 0 of the canvasParentFrame
childFrame1.grid(row=1, column=0, sticky="nesw")    #Places the childFrame1 in row 1 of the canvasParentFrame

#Add that new frame to a window in the canvas
myCanvas.create_window((0,0), window=canvasParentFrame, anchor="nw")    #Adds a window into the top left corner of the
                                                                        #canvas containing the specified frame
#---------------------------------------------------------------------------------------------------------------------------------

#Add new meal code ---------------------------------------------------------------------------------------------------------------

#This function creates the add new meal window when it is called
def createMealGuiFunc(statementType, currentMealName, currentMealServings, currentMealInstructions, currentMealImgDir,
                      currentMealIngredientsNameArray, currentMealIngredientsGramsArray):
    global newMealWinOpen
    global addMealCurrentRoot

    
    if newMealWinOpen == False:     #Used to check if the new meal window already exists and if it doesn't then creates it
        newMealWinOpen = True   #Set to true so that multiple iterations of the new meal window cant be open
        newIngredientWinOpen = False
        currentPopup = None
        currentMealID = None        #This variable is used when the windows is been used to update an aready existing
                                    #meals values so that the correct meal can be updated
    
        newMealRoot = Tk()
        newMealRoot.rowconfigure(0, weight=1)
        newMealRoot.columnconfigure(0, weight=1)
        newMealRoot.geometry("720x800")

        if statementType == 0:      #This if statement is used to change the title of the window depending on if the
                                    #window has been called for creating a new meal or for editing a meal
            newMealRoot.title("Add New Meal")
        elif statementType == 1:
            newMealRoot.title("Edit Meal")
            #Used to get the id of the meal that need updating
            currentMealID = readDBQuery('SELECT id FROM meals WHERE name = "' + str(currentMealName) + '" AND img_dir = "'
                                        + str(currentMealImgDir) + '";')
            currentMealID = currentMealID[0][0]

        addMealCurrentRoot = newMealRoot
        
        #Setup the add meal main frame, add meal canvas, add meal scrollbar and child frames -------------------------------------

        #Create a main frame
        addMealMainFrame = Frame(newMealRoot)
        addMealMainFrame.grid(row=0, column=0, sticky="nesw")
        addMealMainFrame.rowconfigure(index=0, weight=1)        #Set the row and column weight so that the frames
                                                                #that are added scale to the whole window
        addMealMainFrame.columnconfigure(index=0, weight=1)

        #Creates a canvas
        addMealCanvas = Canvas(addMealMainFrame, highlightthickness=0)      #Highlight thickness is set to 0 so that a border
                                                                            #doesn't appear when a user click into an entry box
        addMealCanvas.grid(row=0, column=0, sticky="nesw")

        #Adds a scrollbar to the canvas
        #Orient the scrollbar vertically and assign it to scroll in the y axis
        addMealScrollbar = Scrollbar(addMealMainFrame, orient=VERTICAL, command=addMealCanvas.yview)    
        addMealScrollbar.grid(row=0, column=1, sticky="ns")  #Places the scrollbar in column 1 as the canvas is in column 0

        #Configure the canvas
        addMealCanvas.configure(yscrollcommand=addMealScrollbar.set)      #Links the canvas with the scrollbar
        #Set the Bbox so the scoll bar knows the scroll region when the scroll bar is first added to the canvas
        addMealCanvas.bind("<Configure>", lambda e: addMealCanvas.configure(scrollregion = addMealCanvas.bbox("all")))

        #Create the frames for inside the canvas
        addMealCanvasParentFrame = Frame(addMealCanvas)
        addMealFrame = Frame(addMealCanvasParentFrame)

        addMealFrame.grid(row=0, column=0, sticky="nesw")    #Places the childFrame1 in row 1 of the addMealCanvasParentFrame

        #Add that new frame to a window in the canvas
        addMealCanvas.create_window((0,0), window=addMealCanvasParentFrame, anchor="nw")    #Adds a window into the top left
                                                                                            #corner of the canvas containing
                                                                                            #the specified frame
        #-------------------------------------------------------------------------------------------------------------------------


        def addMeaIUpdateBbox():    #This function is used to update the Bbox for the scrollbar so that the scroll will
                                    #scroll to the correct location in the yaxis after the widgets have been resized
            addMealCanvas.configure(scrollregion=addMealCanvas.bbox("all"))

        def submitBtnFunc(nameObj, isLiquidObj, energyObj, fatObj, satFatObj, carbsObj, sugarObj, fibreObj, proteinObj, saltObj,
                          vitaminAObj, thiaminObj, riboflavinObj, niacinObj, vitaminB6Obj, vitaminB12Obj, vitaminCObj,
                          vitaminDObj, calciumObj, phosphorusObj, magnesiumObj, potassiumObj, ironObj, zincObj, copperObj,
                          seleniumObj):
            
            validData = True

            #Gets all the values that are in the nutrition entry boxes
            name = nameObj.get()
            isLiquid = isLiquidObj.get()
            energy = energyObj.get()
            fat = fatObj.get()
            satFat = satFatObj.get()
            carbs = carbsObj.get()
            sugar = sugarObj.get()
            fibre = fibreObj.get()
            protein = proteinObj.get()
            salt = saltObj.get()
            vitaminA = vitaminAObj.get()
            thiamin = thiaminObj.get()
            riboflavin = riboflavinObj.get()
            niacin = niacinObj.get()
            vitaminB6 = vitaminB6Obj.get()
            vitaminB12 = vitaminB12Obj.get()
            vitaminC = vitaminCObj.get()
            vitaminD = vitaminDObj.get()
            calcium = calciumObj.get()
            phosphorus = phosphorusObj.get()
            magnesium = magnesiumObj.get()
            potassium = potassiumObj.get()
            iron = ironObj.get()
            zinc = zincObj.get()
            copper = copperObj.get()
            selenium = seleniumObj.get()

            nutrientValuesObjArray = [energyObj, fatObj, satFatObj, carbsObj, sugarObj, fibreObj, proteinObj, saltObj, vitaminAObj,
                          thiaminObj, riboflavinObj, niacinObj, vitaminB6Obj, vitaminB12Obj, vitaminCObj, vitaminDObj, calciumObj,
                          phosphorusObj, magnesiumObj, potassiumObj, ironObj, zincObj, copperObj, seleniumObj]

            nutrientValuesArray = [energy, fat, satFat, carbs, sugar, fibre, protein, salt, vitaminA, thiamin, riboflavin, niacin,
                                   vitaminB6, vitaminB12, vitaminC, vitaminD, calcium, phosphorus, magnesium, potassium, iron,
                                   zinc, copper, selenium]


            if name == "":
                nameObj.config(fg="red")
                nameObj.insert(0,"Required")
                validData = False
            else:     
                if name == "null" or name == "Required":
                    nameObj.config(fg="red")
                    validData = False
                else:
                    if name == "Too long":
                        nameObj.config(fg="red")
                        validData = False
                    else:
                        print("Name =", name)
                        if len(name) > 50:      #Stops the name from been over 50 characters as that is the limit for the database
                            nameObj.config(fg="red")
                            nameObj.delete(0, "end")
                            nameObj.insert(0,"Too long")
                            validData = False
                        else:
                            try:    #Used to test if the name is made of characters and not a number
                                temp = float(name)
                                nameObj.config(fg="red")
                                validData = False
                            except:
                                if name != "Ingredient Of Such Name Already Exists":
                                    checkNameResult = readDBQuery('SELECT id FROM ingredients WHERE name = "' + str(name) + '";')

                                    if len(checkNameResult) != 0:
                                        nameObj.config(fg="red")
                                        nameObj.delete(0, "end")
                                        nameObj.insert(0,"Ingredient Of Such Name Already Exists")
                                        validData = False
                                    else:
                                        nameObj.config(fg="black")  
                                                        
                                    

            if isLiquid == "":
                isLiquidObj.config(fg="red")
                isLiquidObj.insert(0,"Required")
                validData = False
            else:
                if isLiquid == "null" or isLiquid == "Required":
                    isLiquidObj.config(fg="red")
                else:
                    if (isLiquid != "yes" and isLiquid != "Yes" and isLiquid != "y" and isLiquid != "Y" and isLiquid != "no"
                        and isLiquid != "No" and isLiquid != "n" and isLiquid != "N"):
                        isLiquidObj.config(fg="red")
                        isLiquidObj.delete(0, "end")
                        isLiquidObj.insert(0,"Must be Yes or No")
                    else:
                        isLiquidObj.config(fg="black")


            for i in range (0, len(nutrientValuesArray)):       #Used to ensure the values are numbers and that
                                                                #the ingredient isn't blank, 
                if nutrientValuesArray[i] == "":
                    nutrientValuesObjArray[i].config(fg="red")
                    nutrientValuesObjArray[i].insert(0, "Required")
                    validData = False
                else:
                    if nutrientValuesArray[i] != "null":
                        try:
                            temp = float(nutrientValuesArray[i])
                            nutrientValuesObjArray[i].config(fg="black")
                        except:
                            nutrientValuesObjArray[i].config(fg="red")
                            validData = False
                    else:
                        nutrientValuesObjArray[i].config(fg="black")


            if isLiquid == "Yes" or isLiquid == "yes" or isLiquid == "y" or isLiquid == "Y":    #Changes the isLiquid value to
                                                                                                #1 or 0 for the format needed for
                                                                                                #the ingredients table
                isLiquid = "true"
            elif isLiquid == "No" or isLiquid == "no" or isLiquid == "n" or isLiquid == "N":
                isLiquid = "false"

            if validData == True:
                ingredientName = str(name)

                tempSplitName = name.split(" ")
                tempSplitName[0].title()    #Used to make sure the first chanracter in the ingredient name is a capital

                ingredientName = ""
                for k in range(0, len(tempSplitName)):
                    if k == (len(tempSplitName) - 1):
                        ingredientName =  ingredientName + tempSplitName[k]
                    else:
                        ingredientName =  ingredientName + tempSplitName[k] + " "

                updateIngredientDropdownFunc(ingredientName)    #Calls the function that will add the
                                                                #new ingredient to the dropdown

                insert_ingredients_query = """
                    INSERT INTO ingredients (name, is_liquid, energy, fat, sat_fat, carbs, sugar, fibre, protein, salt, vit_a,
                    thiamin, riboflavin, niacin, vit_b6, vit_b12, vit_c, vit_d, calcium, phosphorus, magnesium, potassium,
                    iron, zinc, copper, selenium)
                    VALUES
                        ("""
                insert_string = '"'+ ingredientName + '"' + "," + str(isLiquid) + "," + str(energy) + "," + str(fat) + ","
                + str(satFat) + "," + str(carbs) + "," + str(sugar) + "," + str(fibre) + "," + str(protein) + "," + str(salt)
                + "," + str(vitaminA) + "," + str(thiamin) + "," + str(riboflavin) + "," + str(niacin) + "," +str(vitaminB6)
                + "," + str(vitaminB12) + "," + str(vitaminC) + "," + str(vitaminD) + "," + str(calcium) + "," + str(phosphorus)
                + "," + str(magnesium) + "," + str(potassium) + "," + str(iron) + "," + str(zinc) + "," + str(copper)
                + "," + str(selenium) + ");"

                insert_ingredients_query = insert_ingredients_query + insert_string

                print(insert_ingredients_query)
                writeDBQuery(insert_ingredients_query)

                #Clears all the entry boxes
                nameObj.delete(0, "end")
                isLiquidObj.delete(0, "end")
                energyObj.delete(0, "end")
                fatObj.delete(0, "end")
                satFatObj.delete(0, "end")
                carbsObj.delete(0, "end")
                sugarObj.delete(0, "end")
                fibreObj.delete(0, "end")
                proteinObj.delete(0, "end")
                saltObj.delete(0, "end")
                vitaminAObj.delete(0, "end")
                thiaminObj.delete(0, "end")
                riboflavinObj.delete(0, "end")
                niacinObj.delete(0, "end")
                vitaminB6Obj.delete(0, "end")
                vitaminB12Obj.delete(0, "end")
                vitaminCObj.delete(0, "end")
                vitaminDObj.delete(0, "end")
                calciumObj.delete(0, "end")
                phosphorusObj.delete(0, "end")
                magnesiumObj.delete(0, "end")
                potassiumObj.delete(0, "end")
                ironObj.delete(0, "end")
                zincObj.delete(0, "end")
                copperObj.delete(0, "end")
                seleniumObj.delete(0, "end")
                        

        def readIngredientsFunc():  #This function reads all of the ingredient names from the ingredients table
            tempIngredientArray = []
            
            get_ingredients_query = """
                SELECT name FROM ingredients"""

            result = readDBQuery(get_ingredients_query)
            for x in range(0, len(result)):     #Gets the ingredients that were returned from the database query
                tempIngredientArray.append(result[x][0])
                        
            tempIngredientArray.sort()     #This line sorts the array into alphabetical order
            return tempIngredientArray

        def newIngredientFunc():
            nonlocal newIngredientWinOpen
            nonlocal currentPopup

            POPUP_PREV_HEIGHT = 0       #Used to store the popup height the last time it was resized
            POPUP_ADD_MEAL_NEED_RESIZE = False  #Used to store a boolean value so that the popup resize function doesn't
                                                #get run mulitiple times due to both the screen changing size and the
                                                #mouse entering the popup having the potential to the ultimatly
                                                #trigger the resize function
            
            if newIngredientWinOpen == False:
                newIngredientWinOpen = True
                popup = Toplevel(addMealFrame)
                popup.title("Add New Ingredient")
                currentPopup = popup

                #Nutriton labels
                nameLabel = Label(popup, text="Name")
                isLiquidLabel = Label(popup, text="Is it Liquid")
                energyLabel = Label(popup, text="Energy(kcal)")
                fatLabel = Label(popup, text="Fat(g)")
                satFatLabel = Label(popup, text="Saturated Fat(g)")
                carbsLabel = Label(popup, text="Carbohydrates(g)")
                sugarLabel = Label(popup, text="Sugar(g)")
                fibreLabel = Label(popup, text="Fibre(g)")
                proteinLabel = Label(popup, text="Protein(g)")
                saltLabel = Label(popup, text="Salt(g)")
                vitaminALabel = Label(popup, text="Vitamin A(µg)")
                thiaminLabel = Label(popup, text="Thiamin(mg)")
                riboflavinLabel = Label(popup, text="Riboflavin(mg)")
                niacinLabel = Label(popup, text="Niacin(mg)")
                vitaminB6Label = Label(popup, text="Vitamin B6(mg)")
                vitaminB12Label = Label(popup, text="Vitamin B12(µg)")
                vitaminCLabel = Label(popup, text="Vitamin C(mg)")
                vitaminDLabel = Label(popup, text="Vitamin D(µg)")
                calciumLabel = Label(popup, text="Calcium(mg)")
                phosphorusLabel = Label(popup, text="Phosphorus(mg)")
                magnesiumLabel = Label(popup, text="Magnesium(mg)")
                potassiumLabel = Label(popup, text="Potassium(mg)")
                ironLabel = Label(popup, text="Iron(mg)")
                zincLabel = Label(popup, text="Zinc(mg)")
                copperLabel = Label(popup, text="Copper(mg)")
                seleniumLabel = Label(popup, text="Selenium(µg)")

                #Nutrition entry boxes
                nameEntry = Entry(popup, width=40)
                isLiquidEntry = Entry(popup, width=40)
                energyEntry = Entry(popup, width=40)
                fatEntry = Entry(popup, width=40)
                satFatEntry = Entry(popup, width=40)
                carbsEntry = Entry(popup, width=40)
                sugarEntry = Entry(popup, width=40)
                fibreEntry = Entry(popup, width=40)
                proteinEntry = Entry(popup, width=40)
                saltEntry = Entry(popup, width=40)
                vitaminAEntry = Entry(popup, width=40)
                thiaminEntry = Entry(popup, width=40)
                riboflavinEntry = Entry(popup, width=40)
                niacinEntry = Entry(popup, width=40)
                vitaminB6Entry = Entry(popup, width=40)
                vitaminB12Entry = Entry(popup, width=40)
                vitaminCEntry = Entry(popup, width=40)
                vitaminDEntry = Entry(popup, width=40)
                calciumEntry = Entry(popup, width=40)
                phosphorusEntry = Entry(popup, width=40)
                magnesiumEntry = Entry(popup, width=40)
                potassiumEntry = Entry(popup, width=40)
                ironEntry = Entry(popup, width=40)
                zincEntry = Entry(popup, width=40)
                copperEntry = Entry(popup, width=40)
                seleniumEntry = Entry(popup, width=40)

                submitBtn = Button(popup, text="Submit", command=lambda: submitBtnFunc(nameEntry, isLiquidEntry, energyEntry,
                                                                                       fatEntry, satFatEntry, carbsEntry,
                                                                                       sugarEntry, fibreEntry, proteinEntry,
                                                                                       saltEntry, vitaminAEntry, thiaminEntry,
                                                                                       riboflavinEntry, niacinEntry,
                                                                                       vitaminB6Entry, vitaminB12Entry,
                                                                                       vitaminCEntry, vitaminDEntry, calciumEntry,
                                                                                       phosphorusEntry, magnesiumEntry,
                                                                                       potassiumEntry, ironEntry, zincEntry,
                                                                                       copperEntry, seleniumEntry))
                submitBtn.grid(row=26, column=1, padx=(0,40), pady=(4,66))

                tempIngredientLabelArray = [nameLabel, isLiquidLabel, energyLabel, fatLabel, satFatLabel, carbsLabel, sugarLabel,
                                            fibreLabel, proteinLabel, saltLabel, vitaminALabel, thiaminLabel, riboflavinLabel,
                                            niacinLabel, vitaminB6Label, vitaminB12Label, vitaminCLabel, vitaminDLabel,
                                            calciumLabel, phosphorusLabel, magnesiumLabel, potassiumLabel, ironLabel, zincLabel,
                                            copperLabel, seleniumLabel]
                tempIngredientEntryArray = [nameEntry, isLiquidEntry, energyEntry, fatEntry, satFatEntry, carbsEntry, sugarEntry,
                                            fibreEntry, proteinEntry, saltEntry, vitaminAEntry, thiaminEntry, riboflavinEntry,
                                            niacinEntry, vitaminB6Entry, vitaminB12Entry, vitaminCEntry, vitaminDEntry,
                                            calciumEntry, phosphorusEntry, magnesiumEntry, potassiumEntry, ironEntry, zincEntry,
                                            copperEntry, seleniumEntry]

                for labelIndexForGrid in range(0, len(tempIngredientLabelArray)):       #This for loop places all the nutrion
                                                                                        #labels onto the popup grid
                    if labelIndexForGrid == 0:
                        tempIngredientLabelArray[labelIndexForGrid].grid(row=int(labelIndexForGrid), column=0, padx=5, pady=(40,4))
                    else:
                        tempIngredientLabelArray[labelIndexForGrid].grid(row=int(labelIndexForGrid), column=0, padx=5, pady=4)

                for entryIndexForGrid in range(0, len(tempIngredientEntryArray)):       #This for loop places all the nutrion
                                                                                        #entry boxes onto the popup grid
                    if entryIndexForGrid == 0:
                        tempIngredientEntryArray[entryIndexForGrid].grid(row=int(entryIndexForGrid), column=1, padx=(0,40),
                                                                         pady=(40,4))
                    else:
                        tempIngredientEntryArray[entryIndexForGrid].grid(row=int(entryIndexForGrid), column=1, padx=(0,40),
                                                                         pady=4)
                    

                def popupaddMealResizeFunc():   #This function is responsible for resizing the widgets
                                                #to the size of the popup height
                    nonlocal POPUP_ADD_MEAL_NEED_RESIZE     #Needed so that it can be set back to false after resizing the
                                                            #widgets so that the widgets don't get unnecessarily
                                                            #scaled multiple times

                    canvas_height = popup.winfo_height()    #Stores the current height of the canvas

                    popupScaleValue = canvas_height / 886   #Calculates the scale value using the start size of the
                                                            #popup height and the actual popup height

                    for ingredientLabelIndex in range(0, len(tempIngredientLabelArray)):
                        #Scales the font size of the popup labels
                        tempIngredientLabelArray[ingredientLabelIndex].config(font=("Times New Roman", int(9 * popupScaleValue)))
                        #Scales the font size of the popup entry boxes
                        tempIngredientEntryArray[ingredientLabelIndex].config(font=("Times New Roman", int(9 * popupScaleValue)))

                        if ingredientLabelIndex == 0:   #If true then it scales the y padding of the
                                                        #first popup label and entry box
                            if canvas_height < 506:     #These if statements adjust the base y padding
                                                        #depending on the popups height
                                if canvas_height < 352:
                                    tempIngredientLabelArray[ingredientLabelIndex].grid(pady=(int(1 * popupScaleValue),
                                                                                              int(4 * popupScaleValue)))
                                    tempIngredientEntryArray[ingredientLabelIndex].grid(pady=(int(1 * popupScaleValue),
                                                                                              int(4 * popupScaleValue)))
                                else:
                                    tempIngredientLabelArray[ingredientLabelIndex].grid(pady=(int(10 * popupScaleValue),
                                                                                              int(4 * popupScaleValue)))
                                    tempIngredientEntryArray[ingredientLabelIndex].grid(pady=(int(10 * popupScaleValue),
                                                                                              int(4 * popupScaleValue)))
                            else:
                                tempIngredientLabelArray[ingredientLabelIndex].grid(pady=(int(40 * popupScaleValue),
                                                                                          int(4 * popupScaleValue)))
                                tempIngredientEntryArray[ingredientLabelIndex].grid(pady=(int(40 * popupScaleValue),
                                                                                          int(4 * popupScaleValue)))
                        else:
                            tempIngredientLabelArray[ingredientLabelIndex].grid(pady=(int(4 * popupScaleValue)))
                            tempIngredientEntryArray[ingredientLabelIndex].grid(pady=(int(4 * popupScaleValue)))


                    submitBtn.config(font=("Times New Roman", int(9 * popupScaleValue)))
                    submitBtn.grid(pady=(int(4 * popupScaleValue),int(66 * popupScaleValue)))
                
                    print("Ingredient window size changed")

                    POPUP_ADD_MEAL_NEED_RESIZE = False

                def popupaddMealCheckaddMealResizeFunc():   #Checks the windows previous known height with the current known
                                                            #height so that the widgets arn't resized when they don't need to be
                    nonlocal POPUP_PREV_HEIGHT
                    popup_height = int(popup.winfo_height())    #Stores the current height of the popup

                    if popup_height > 1:
                        if POPUP_PREV_HEIGHT != popup_height:
                            POPUP_PREV_HEIGHT = popup_height    #Save the popup height to the POPUP_PREV_HEIGHT variable
                            return True

                def popupaddMealResizeAfterTimeFunc():
                    nonlocal POPUP_ADD_MEAL_NEED_RESIZE

                    #This if statment checks that the POPUP_ADD_MEAL_NEED_RESIZE variable is still true as the resizing of the
                    #widgets could have already been triggered by the mouse entering the popup meaning that the
                    #POPUP_ADD_MEAL_NEED_RESIZE variable would thus be False as the widgets would no longer need resizing
                    if POPUP_ADD_MEAL_NEED_RESIZE == True:
                        popupaddMealResizeFunc()

                def popupaddMealWindowSizeChangeFunc(e):
                    nonlocal POPUP_ADD_MEAL_NEED_RESIZE

                    popupResizeBool = popupaddMealCheckaddMealResizeFunc()  #Calls the function to see if the
                                                                            #popup height has changed

                    if popupResizeBool == True:     #This if stement check if the popupaddMealCheckaddMealResizeFunc has
                                                    #returned True meaning that the widgets do need resizing
                        if POPUP_ADD_MEAL_NEED_RESIZE != True:  #Checks that the POPUP_ADD_MEAL_NEED_RESIZE variable isn't already
                                                                #true as the mouse entering the popup could have already cause
                                                                #it to become true
                            POPUP_ADD_MEAL_NEED_RESIZE = True
                            
                        newMealRoot.after(600, popupaddMealResizeAfterTimeFunc)     #Used so that the widgets are resized after
                                                                                    #half a second if the mouse hasn't already
                                                                                    #triggered a resize by entering the popup

                def popupaddMealMouseEnterFunc(e):     #This function is triggered whenever the mouse enters the popup
                    nonlocal POPUP_ADD_MEAL_NEED_RESIZE

                    if POPUP_ADD_MEAL_NEED_RESIZE == True:
                        popupaddMealResizeFunc()


                popup.bind("<Configure>", popupaddMealWindowSizeChangeFunc)
                popup.bind("<Enter>", popupaddMealMouseEnterFunc)
            else:       #This will run if the popup window already exists
                if currentPopup.state() == "iconic":    #Checks if the popup window exists but has been minised
                    currentPopup.deiconify()    #Unminises the popup window

            def popupCloseFunc():
                nonlocal newIngredientWinOpen
                nonlocal currentPopup
                print("Popup window closed")
                newIngredientWinOpen = False
                currentPopup.destroy()      #Used to destroy the popup window when the close button is clicked
                currentPopup = None

            currentPopup.protocol("WM_DELETE_WINDOW", popupCloseFunc)


        def getIngredientId():      #This function changes the names of the ingredients in the
                                    #mealIngreadientsArray to there corrosponding id values
            for i in range (0, len(mealIngredientsArray)):
                get_ingredient_id_query = """
                SELECT id FROM ingredients
                WHERE name = """

                tempStr = mealIngredientsArray[i]
                tempStr = tempStr.split(",")
                strPt1 = tempStr[0]
                strPt1 = strPt1[1:]
                strPt2 = tempStr[1]
                            
                ingredientString = '"' + str(strPt1) + '";'

                get_ingredient_id_query = get_ingredient_id_query + ingredientString

                result = readDBQuery(get_ingredient_id_query)

                for x in range(0, len(result)):
                    temp = str(result[x][0])
                            
                mealIngredientsArray[i] = ("(" + str(temp) + ", " + str(strPt2))


        def repostionAfterRemovalFunc(index):   #This function repositions the labels and remove buttons and the
                                                #submit button when an ingredient is removed from the list
            nonlocal queryLabelArray
            nonlocal removeIngredientBtnArray


            for i in range (index, len(queryLabelArray)):   #This if statement removes all the labels from the grid
                                                            #that were below the label that has been removed
                queryLabelArray[i].grid_forget()

            for i in range (index, len(removeIngredientBtnArray)):  #This if statement removes all the remove buttons from the
                                                                    #grid that were below the remove buttont that has been removed
                removeIngredientBtnArray[i].grid_forget()


            for i in range (index, len(queryLabelArray)):       #This if statement adds the labels that were removed
                                                                #aboved back into the grid in there new positions 
                queryLabelArray[i].grid(row=((i+ 8)), column=2, padx=0, pady=(0,10))

            for i in range (index, len(removeIngredientBtnArray)):      #This if statement adds the remove buttons that were
                                                                        #removed above back into the grid in there new positions
                removeIngredientBtnArray[i].grid(row=(i + 8), column=3, padx=0, pady=(0,10))

            submitMealBtn.grid_forget()     #Removes the submit button from the grid
            submitMealBtn.grid(row=(len(queryLabelArray) + 8), column=2, padx=10, pady=(0,10))  #Adds the submit button back to
                                                                                                #the grid 1 row down to account
                                                                                                #for the new label

            newMealRoot.after(200, addMeaIUpdateBbox)   #Updates the Bbox for the scrollbar after a small time delay so that the
                                                        #changes in widgets have time to be implimented before the Bbox is updated

        def addToOptionMenuFunc(var):       #This function is used to add the variable that was pass to it to the option menu
            nonlocal dropDownIngredientVar

            menu = ingredientsDropDown["menu"]      #Need to acces the parent menu class of the
                                                    #menubutton class that is used by the optionMenu
            menu.add_command(label=str(var), command= lambda: dropDownIngredientVar.set(str(var)))

        def updateIngredientDropdownFunc(tempLabelIngredient):
            nonlocal ingredientArray

            #menu = ingredientsDropDown["menu"]     #Need to acces the parent menu class of the
                                                    #menubutton class that is used by the optionMenu

            tempIngredientArray = ingredientArray
            tempIngredientArray.append(tempLabelIngredient)
            tempIngredientArray = sorted(tempIngredientArray)

            ingredientsDropDown["values"] = tempIngredientArray

            #menu.delete(0, "end")       #Clears all of the ingredients from the option menu

            #for i in range (0, len(tempIngredientArray)):
                #addToOptionMenuFunc(tempIngredientArray[i])

            ingredientArray = tempIngredientArray       #Updates the nonlocal ingredient array so that the newly added ingredient
                                                        #from the remove action / new adding action has been added back

        def removeIngredientFunc(clickedBtnObj):        #This function is responsible for removing the button
                                                        #that was clicked and the label that corresponds to it
            nonlocal queryLabelArray
            nonlocal removeIngredientBtnArray
            nonlocal mealIngredientsArray
            nonlocal ingredientArray

            btnPosition = -1

            for i in range (0, len(removeIngredientBtnArray)):
                if str(clickedBtnObj) == str(removeIngredientBtnArray[i]):      #Used to find where in the array the
                                                                                #button to be removed is
                    btnPosition = i

                    removeIngredientBtnArray[i].grid_forget()
                    queryLabelArray[i].grid_forget()

            if btnPosition >= 0:        #This if statment removes the removed label and button from the
                                        #removeIngredientBtnArray and the queryLabelArray
                tempLabelIngredient = queryLabelArray[btnPosition].cget("text")     #Gets the name of the ingredient that
                                                                                    #needs to be removed using the
                                                                                    #value in the given label  
                tempLabelIngredient = tempLabelIngredient.split(",")
                tempLabelIngredient = tempLabelIngredient[0]
                tempLabelIngredient = tempLabelIngredient[1:]

                updateIngredientDropdownFunc(tempLabelIngredient)       #Calls the function that adds the
                                                                        #ingredient back to the dropdown

                del mealIngredientsArray[btnPosition]       #Removes the ingredient that was added back to the
                                                            #dropdown from the mealIngredient array

                del removeIngredientBtnArray[btnPosition]       #Removes the remove button that corresponds to the
                                                                #ingredient that was added back to the dropdown

                del queryLabelArray[btnPosition]                #Removes the query label that corresponds to the
                                                                #ingredient that was added back to the dropdown

            repostionAfterRemovalFunc(btnPosition)      #This function is called to reposition the other widgets in
                                                        #the window to account for the removed label and button


        queryLabelArray = []
        removeIngredientBtnArray = [] 

        def addIngredienToGuiFunc(ingredientName, enteredAmount):       #This function is used when adding a new meal
                                                                        #and editing a meal to add the meals
                                                                        #ingredients to the gui
            nonlocal dropDownIngredientVar
            nonlocal ingredientArray
            nonlocal queryLabelArray
            nonlocal removeIngredientBtnArray
            
            canvas_width = addMealCanvas.winfo_width()    #Stores the current width of the canvas
            scaleValue = (canvas_width / 720)
                        
            temp = float(enteredAmount)     #Used to test that the grams amount entered consists of only numbers

            #Adds the ingredients values to the nonlocal mealIngredientsArray
            mealIngredientsArray.append("(" + str(ingredientName) + ", " + str(enteredAmount) + "),")

            mealAddQuery = Label(addMealFrame, text=str(mealIngredientsArray[-1]))
            mealAddQuery.config(font=("Times New Roman", int(10 * scaleValue)))
            queryLabelArray.append(mealAddQuery)       #Adds the meal label to the array
            #Places the new label object into the grid
            queryLabelArray[-1].grid(row=(len(queryLabelArray) + 7), column=2, padx=0, pady=(0,10))

            remove_btn = Button(addMealFrame, text="Remove", command= lambda: removeIngredientFunc(remove_btn))
            remove_btn.config(font=("Times New Roman", int(10 * scaleValue)))
            remove_btn.grid(row=(len(queryLabelArray) + 7), column=3, padx=0, pady=(0,10))
            removeIngredientBtnArray.append(remove_btn)
                        
            submitMealBtn.grid_forget()     #Removes the submit button from the grid
            #Adds the submit button back to the grid 1 row down to account for the new label
            submitMealBtn.grid(row=(len(queryLabelArray) + 8), column=2, padx=10, pady=(0,10))
                        


            temp = []
            for i in range (0, len(ingredientArray)):
                if str(ingredientArray[i]) != str(ingredientName):
                    temp.append(ingredientArray[i])

            ingredientsDropDown["values"] = temp

            ingredientArray = temp
            dropDownIngredientVar.set("Select ingredient")  #Resets the default value for the ingredient optionMenu
            amountEntry.delete(0, "end")        #Removes all values from the amount entry box so that the entry box is
                                                #empty after the ingredient has been added
            amountEntry.config(fg="black")      #Turns it back to black incase the text has been changed to red
            newMealRoot.after(200, addMeaIUpdateBbox)   #Updates the Bbox for the scrollbar after a small time
                                                        #delay so that the changes in widgets have time to be
                                                        #implimented before the Bbox is updated 

        def addMealIngredientFunc():        #This function is triggered when a user clicks the add
                                            #button to add an ingredient to the meal
            nonlocal dropDownIngredientVar
            
            enteredAmount = amountEntry.get()
            ingredientName = str(dropDownIngredientVar.get())
            

            if ingredientName == "Select ingredient":   #This if statement is used to stop the default value of
                                                        #the dropdownmenu from been added as an ingredient
                ingredientsDropDown.config(foreground="red")
            else:
                ingredientsDropDown.config(foreground="black")
                
                if enteredAmount == "":     #This if and try is used to ensure there is a value in the amount
                                            #entry box and that the value is a number and not characters
                    amountEntry.config(fg="red")
                    amountEntry.insert(0, "Required")
                elif enteredAmount == "0":
                    amountEntry.config(fg="red")
                else:
                    try:
                        addIngredienToGuiFunc(ingredientName, enteredAmount)
                    except:
                        amountEntry.config(fg="red")

        def submitMealBtnFunc():
            nonlocal removeIngredientBtnArray
            
            mealDBName = mealEntryName.get()        #This variable stores the proposed name for the meal
            numServings = numServingsEntry.get()    #This variable stores the number of servings for the meal
            imgDir = imgDirEntry.get()              #This variable stores the image directory for the meals image
            
            instructionsVar = instructionsText.get("1.0", "end-1c")     #This variable stores the instructions for the meal
            instructionsVar = instructionsVar.strip()
                    

            if mealDBName == "":
                mealEntryName.config(fg="red")
                mealEntryName.insert(0,"Required")
            else:
                if mealDBName == "null" or mealDBName == "Required":
                    mealEntryName.config(fg="red")
                else:
                    #Checks that the meal name isn't over 50 as that is the limit for the database
                    if len(mealDBName) > 50:
                        mealEntryName.config(fg="red")
                        mealEntryName.delete(0, "end")
                        mealEntryName.insert(0,"Too long")
                    else:
                        if mealDBName == "Too long":
                            mealEntryName.config(fg="red")
                        else:
                            try:    #Used to test if the name is made of characters and not a number
                                temp = float(mealDBName)
                                mealEntryName.config(fg="red")
                            except:
                                mealEntryName.config(fg="black")        #Gets to this point if the meal name was ok
                                
                                if numServings == "":
                                    numServingsEntry.config(fg="red")
                                    numServingsEntry.insert(0, "Required")
                                else:
                                    try:
                                        temp = float(numServings)
                                        #Gets to this point if the number of servings entry was ok
                                        numServingsEntry.config(fg="black") 

                                        if imgDir == "":
                                            imgDirEntry.config(fg="red")
                                            imgDirEntry.insert(0, "Required")
                                        else:
                                            if imgDir != "Required":
                                                try:
                                                    temp = float(imgDir)
                                                    imgDirEntry.config(fg="red")
                                                except:
                                                    imageExists = exists(str(imgDir))

                                                    if imageExists == False:
                                                        imgDirEntry.config(fg="red")
                                                        imgDirEntry.delete(0, "end")
                                                        imgDirEntry.insert(0, "Invalid directory")
                                                    else:
                                                        #Gets to this point if the image dir entry was ok
                                                        imgDirEntry.config(fg="black")

                                                        #Removes any white space from the start and end of the string
                                                        mealDBName = mealDBName.strip()
                                                        #Replaces any underscores in the table name with spaces
                                                        mealDBName = mealDBName.replace("_", " ")
                                                        #Replaces any spaces in the table name with underscores
                                                        #mealDBName = mealDBName.replace(" ", "_")

                                                        mealNameResults = None

                                                        if statementType == 0:
                                                            #Checks if a meal already exists with the given name
                                                            mealNameResults = readDBQuery('SELECT id FROM meals WHERE name = "'
                                                                                          +  str(mealDBName) + '";')
                                                        elif statementType == 1:
                                                            if str(mealDBName) != currentMealName:
                                                                #Checks if a meal already exists with the given name
                                                                mealNameResults = readDBQuery('SELECT id FROM meals WHERE name = "'
                                                                                              +  str(mealDBName) + '";')
                                                            else:
                                                                mealNameResults = ""

                                                        mealExists = False

                                                        if len(mealNameResults) > 0:
                                                            mealExists = True

                                                        if mealExists == False:
                                                            mealID = 0
                                                            #Gets the number of rows that are in the meals table
                                                            numRows = readDBQuery('SELECT COUNT(*) FROM meals;')
                                                            #Gets all of the ids that are in the meals table
                                                            allIDs = readDBQuery('SELECT id FROM meals ORDER BY id ASC;')

                                                            #Replaces any breaklines with a hash symbol
                                                            instructionsVar = instructionsVar.replace("\n", "^")
                                                            #instructionsVar = instructionsVar.replace("^^", "^")

                                                            if statementType == 0:
                                                                #This if statement checks if the number of rows in the
                                                                #meal table is the same as the last id value
                                                                if int(numRows[0][0]) != int(allIDs[-1:][0][0]):
                                                                    for k in range(0, len(allIDs)):
                                                                        if mealID == 0:
                                                                            #This if loop finds the first missing
                                                                            #number in the list
                                                                            if (k + 1) != int(allIDs[k][0]):
                                                                                #Sets the mealID to the first id
                                                                                #that is missing from the list
                                                                                mealID = (k + 1)        
                                                                else:
                                                                    mealID = int(allIDs[-1:][0][0]) + 1
                                                            elif statementType == 1:
                                                                mealID = currentMealID


                                                            insertMealQuery =""
                                                            #This if statement is used to decide if the values are added
                                                            #to the meals table of updated in the meals table depening on
                                                            #if the window has been create for adding a new meal or for
                                                            #editing an existing meal
                                                            if statementType == 0:                                                            
                                                                insertMealQuery = ('INSERT INTO meals (id, name, num_servings,'
                                                                + ' instructions, img_dir) VALUES ')
                                                                                   
                                                                mealString = ('(' + str(mealID) + ', "' + str(mealDBName) + '", '
                                                                + str(numServings) + ', "' + instructionsVar + '", "'
                                                                + str(imgDir) + '");')
                                                                
                                                                insertMealQuery = insertMealQuery + mealString
                                                            elif statementType == 1:
                                                                insertMealQuery = 'UPDATE meals SET '
                                                                
                                                                mealString = ('name = "' + str(mealDBName) + '", num_servings = '
                                                                + str(numServings) + ', instructions = "' + instructionsVar
                                                                + '", img_dir = "' + str(imgDir) + '"')
                                                                
                                                                insertMealQuery = (insertMealQuery + mealString + 'WHERE id = '
                                                                + str(currentMealID) + ';')

                                                            writeDBQuery(insertMealQuery)

                                                            print()
                                                            print("insertMealQuery = ", insertMealQuery)
                                                            print()

                                                            #Called so that the ingredients in the array are
                                                            #converted to there corrosponding id values
                                                            getIngredientId()
                                                            
                                                            #This line gets the ingredients that are currently added to the
                                                            #window amd the sorts it in ascending order by ingredient ID
                                                            tempMealGuiResults = sorted(mealIngredientsArray, key=lambda x : x[0])
                                                            #This line reads all of the ingredients that are in
                                                            #the meal_ingredients table for the given meal
                                                            ingredientGramResult = readDBQuery('SELECT ingredient_id, grams_amount'
                                                            + ' FROM meal_ingredients WHERE meal_id = ' + str(mealID) + ';')


                                                            insertIngredientQuery = ('INSERT INTO meal_ingredients (meal_id,'
                                                            + ' ingredient_id, grams_amount) VALUES (')

                                                            #This is true if it is a new meal been added
                                                            if statementType == 0:
                                                                for k in range(0, len(mealIngredientsArray)):
                                                                    print("mealIngredientsArray[k] = ", mealIngredientsArray[k])
                                                                    temp = mealIngredientsArray[k].split(",")
                                                                    #Stores the id of the ingredient
                                                                    ingredientID = str(temp[0])[1:]
                                                                    #Stores to grams amount for the ingredient
                                                                    ingredientGrams = str(temp[1])[:-1] 
                                                                    print(insertIngredientQuery + str(mealID) + ', '
                                                                          + str(ingredientID) + ', ' + str(ingredientGrams) + ');')
                                                                    writeDBQuery(insertIngredientQuery + str(mealID) + ', '
                                                                                 + str(ingredientID) + ', '
                                                                                 + str(ingredientGrams) + ');')
                                                                    #Print the insert for the meal_ingredients table
                                                                    print("(" + str(mealID) + ', ' + str(ingredientID) + ', '
                                                                          + str(ingredientGrams) + '),')
                                                            #This is true if an already exisitng meal is been edited
                                                            elif statementType == 1:
                                                                guiIngredientGramResult = []

                                                                #Coverts the array that stores all the ingredients currently
                                                                #added to the window into a 2 dimensional array
                                                                for resultArrayIndex in range (0, len(tempMealGuiResults)): 
                                                                    tempSplit = tempMealGuiResults[resultArrayIndex].split(",")
                                                                    tempSplit[0] = int(tempSplit[0][1:])
                                                                    tempSplit[1] = float(tempSplit[1].strip()[:-1])
                                                                    #Adds the ingredient id and grams amount to the 2
                                                                    #dimensional array guiIngredientGramResult
                                                                    guiIngredientGramResult.append([tempSplit[0],tempSplit[1]])
                               
                                                                #This for loop is used to check if the ingredients in the
                                                                #ingredients that are in the window are already in
                                                                #the meal_ingredients table
                                                                for guiIngredientIndex in range (0, len(guiIngredientGramResult)):
                                                                    for tableIngredientIndex in range (0, len(ingredientGramResult)):
                                                                        #Checks if the ingredient id matches, meaning that
                                                                        #the ingredient is already in the meal_ingredients
                                                                        #table for the given meal
                                                                        if guiIngredientGramResult[:1][0][0] == ingredientGramResult[tableIngredientIndex][0]:
                                                                            #Checks if the grams amount matches, so that
                                                                            #is can be decided if the ingredients gram
                                                                            #amount need updating or if nothing need
                                                                            #to be done to the entry
                                                                            if guiIngredientGramResult[:1][0][1] == ingredientGramResult[tableIngredientIndex][1]:   
                                                                                del ingredientGramResult[tableIngredientIndex]
                                                                                del guiIngredientGramResult[:1]
                                                                            #This is true if the ingredient is already
                                                                            #in the meal_ingredients table but the
                                                                            #gram amount has changed
                                                                            elif guiIngredientGramResult[:1][0][1] != ingredientGramResult[tableIngredientIndex][1]:
                                                                                writeDBQuery('UPDATE meal_ingredients SET'
                                                                                + 'grams_amount = '
                                                                                + str(guiIngredientGramResult[:1][0][1])
                                                                                + ' WHERE meal_id = ' + str(mealID)
                                                                                + ' AND ingredient_id = '
                                                                                + str(guiIngredientGramResult[:1][0][0]) + ';')
                                                                                del guiIngredientGramResult[:1]
                                                                                del ingredientGramResult[tableIngredientIndex]
                                                                            break
                                                                #This for loop adds all the ingredients that are left
                                                                #in the guiIngredientGramResult array as if they are still
                                                                #in the array at this point then they are new ingredients
                                                                #for the meal and need adding to the meal_ingredients table
                                                                for guiAddIngredientIndex in range (0,len(guiIngredientGramResult)):  
                                                                    writeDBQuery('INSERT INTO meal_ingredients (meal_id,'
                                                                    + 'ingredient_id, grams_amount) VALUES (' + str(mealID)
                                                                    + ',' + str(guiIngredientGramResult[guiAddIngredientIndex][0])
                                                                    + ',' + str(guiIngredientGramResult[guiAddIngredientIndex][1])
                                                                    + ');')

                                                                #Removes all the ingredients from the guiIngredientGramResult
                                                                #array as all of the ingredients have been added to the
                                                                #meal_ingredients table by the for loop above
                                                                guiIngredientGramResult.clear()

                                                                #This for loop deletes all of the ingredients that are left
                                                                #in the ingredientGramResult array as if they are still in
                                                                #the array at this point then they are nolonger in the
                                                                #window meaning that they have been removed from the meal
                                                                for tableDeleteIngredientIndex in range (0, len(ingredientGramResult)): 
                                                                    writeDBQuery('DELETE FROM meal_ingredients WHERE meal_id = '
                                                                    + str(mealID) + ' AND ingredient_id = '
                                                                    + str(ingredientGramResult[tableDeleteIngredientIndex][0])
                                                                    + ';')

                                                                #Removes all the ingredients from the ingredientGramResult
                                                                #array as all of the ingreients that are left in the
                                                                #ingredientGramResult array have been removed from the
                                                                #meal_ingredients table by the for loop above
                                                                ingredientGramResult.clear()    


                                                                #Used to remove all of the ingredient labels and buttons,
                                                                #and to add the ingredients back to the dropdown
                                                            for a in range(0, len(removeIngredientBtnArray)):
                                                                #Pass the last element in the array to the function that
                                                                #will remove the remove btn, ingredent label and add the
                                                                #ingredient back to the dropdown, the function will also
                                                                #remove the object that was passed to the function from
                                                                #the removeIngredientBtnArray and the arry that
                                                                #stores the label
                                                                removeIngredientFunc(removeIngredientBtnArray[-1:][0])       

                                                            #Clears the number of servings from the entry box
                                                            numServingsEntry.delete(0, "end")
                                                            #Clears the name of the meal from the entry box
                                                            mealEntryName.delete(0, "end")
                                                            #Clears the image directory from the entry box
                                                            imgDirEntry.delete(0, "end")
                                                            #Clears the instruction text widget
                                                            instructionsText.delete("1.0", "end")   

                                                            #Updates the Bbox for the scrollbar after a small time delay so
                                                            #that the changes in widgets dimensions have time to be
                                                            #implimented before the Bbox is updated
                                                            newMealRoot.after(200, addMeaIUpdateBbox)     

                                                            if statementType == 0:
                                                                addNewMealFunc(mealDBName, imgDir)
                                                            elif statementType == 1:
                                                                mealValuesTotalArray = mealNutritionValuesFunc(mealID)
                                                                update_meal_nutrition_query = ('UPDATE meal_nutrition SET energy = '
                                                                + str(mealValuesTotalArray[0]) + ', fat = '
                                                                + str(mealValuesTotalArray[1]) + ', sat_fat = '
                                                                + str(mealValuesTotalArray[2]) + ', carbs = '
                                                                + str(mealValuesTotalArray[3]) + ', sugar = '
                                                                + str(mealValuesTotalArray[4]) + ', fibre = '
                                                                + str(mealValuesTotalArray[5]) + ', protein = '
                                                                + str(mealValuesTotalArray[6]) + ', salt = '
                                                                + str(mealValuesTotalArray[7]) + ', vit_a = '
                                                                + str(mealValuesTotalArray[8]) + ', thiamin = '
                                                                + str(mealValuesTotalArray[9]) + ', riboflavin = '
                                                                + str(mealValuesTotalArray[10]) + ', niacin = '
                                                                + str(mealValuesTotalArray[11]) + ', vit_b6 = '
                                                                + str(mealValuesTotalArray[12]) + ', vit_b12 = '
                                                                + str(mealValuesTotalArray[13]) + ', vit_c = '
                                                                + str(mealValuesTotalArray[14]) + ', vit_d = '
                                                                + str(mealValuesTotalArray[15]) + ', calcium = '
                                                                + str(mealValuesTotalArray[16]) + ', phosphorus = '
                                                                + str(mealValuesTotalArray[17]) + ', magnesium = '
                                                                + str(mealValuesTotalArray[18]) + ', potassium = '
                                                                + str(mealValuesTotalArray[19]) + ', iron = '
                                                                + str(mealValuesTotalArray[20]) + ', zinc = '
                                                                + str(mealValuesTotalArray[21]) + ', copper = '
                                                                + str(mealValuesTotalArray[22]) + ', selenium = '
                                                                + str(mealValuesTotalArray[23]) + ' WHERE meal_id = '
                                                                + str(mealID) + ';')
                                                                print(update_meal_nutrition_query)
                                                                writeDBQuery(update_meal_nutrition_query)
                                                                rootCloseFunc()
                                                        else :
                                                            mealEntryName.config(fg="red")
                                                            mealEntryName.delete(0, "end")    #Clears the entry box
                                                            mealEntryName.insert(0,"Meal of name exists already")
                                    except Error as e:
                                        print(e)
                                        numServingsEntry.config(fg="red")
                                


        #This function is triggred when the imgDirBtn button is clicked and is
        #responsible for opening the file explorer so that a user can select an image
        def locateImgBtnFunc():     
            filename = filedialog.askopenfilename(initialdir = "/",
                                                  title = "Select a File",
                                                  filetypes = (("Image files",
                                                                "*.jpg*"),
                                                               ("Image files",
                                                                "*.jpeg*"),
                                                               ("Image files",
                                                                "*.png*"),
                                                               ("all files",
                                                                "*.*")))

            imgDirEntry.config(fg="black")
            imgDirEntry.delete(0, "end")        #Remove anything from the image directory entry box so that it is empty
            imgDirEntry.insert(0, str(filename))    #Adds the submitted file location to the entry box

            #The below lines are used to bring the new meal gui back to the
            #front after it has been sent back by the file explorer 
            newMealRoot.lift()
            newMealRoot.attributes('-topmost',True)
            newMealRoot.after_idle(newMealRoot.attributes,'-topmost',False)

        #This function is called when an ingredient is selected in the dropdown
        #and is used to set the unit for the ingredient amount e.g. g or ml
        def dropdownIngredientSelectedFunc(e):      
            ingredientNameString = dropDownIngredientVar.get()      #Gets the name of the ingredient that was
                                                                    #selected in the ingredient dropdown

            #Gets the is_liquid value for the given ingredient to tell if the ingredient is a liquid
            result = readDBQuery('SELECT is_liquid FROM ingredients WHERE name = "' + str(ingredientNameString) + '";')     

            #This if statement changes the text that is in the amountLabel
            #depending on if the ingredient is or isn't a liquid
            if (int(result[0][0]) == 0):
                amountLabel.config(text="Amount in grams (g)")
            elif (int(result[0][0] == 1)):
                amountLabel.config(text="Amount in milliliters (ml)")
            

        mealIngredientsArray = []       #This array is used to store all of the ingredients
                                        #that the user enters from the option menu


        mealNameLabel = Label(addMealFrame, text="Meal name")
        mealNameLabel.grid(row=0, column=1, padx=(10,0), pady=5)

        mealEntryName = Entry(addMealFrame, width=26)
        mealEntryName.grid(row=0, column=2, padx=0, pady=5)

        numServingsLabel = Label(addMealFrame, text="Number of servings")
        numServingsLabel.grid(row=1, column=1, padx=(10,0), pady=5)

        numServingsEntry = Entry(addMealFrame, width=26)
        numServingsEntry.grid(row=1, column=2, padx=0, pady=5)

        imgDirLabel = Label(addMealFrame, text="Meal image")
        imgDirLabel.grid(row=2, column=1, padx=10, pady=5)

        imgDirEntry = Entry(addMealFrame, width=26)
        imgDirEntry.grid(row=2, column=2, padx=(10,0), pady=5)

        imgDirBtn = Button(addMealFrame, text="Locate image", command=lambda: locateImgBtnFunc())
        imgDirBtn.grid(row=2, column=3, padx=10, pady=5)

        instructionsLabel = Label(addMealFrame, text="Instructions")
        instructionsLabel.grid(row=3, column=1, padx=0, pady=(0,10))

        instructionsText = Text(addMealFrame, height=12, width=75)
        instructionsText.grid(row=4, column=1, columnspan=3, padx=10, pady=(0,5))

        newIngredientBtn = Button(addMealFrame, text="Add new ingredient to dropdown", command=newIngredientFunc)
        newIngredientBtn.grid(row=5, column=2, pady=(20,10))

        ingredientLabel = Label(addMealFrame, text="Ingredient")
        ingredientLabel.grid(row=6, column=1, pady=(0,10))


        ingredientArray =  readIngredientsFunc()        #Calls the function that reads all the ingredients from
                                                        #the database so that they can be added to the optionmenu

        dropDownIngredientVar = StringVar(addMealFrame)
        dropDownIngredientVar.set("Select ingredient")
        ingredientsDropDown = ttk.Combobox(addMealFrame, state="readonly", textvariable= dropDownIngredientVar,
                                           values = ingredientArray, width=40) 
        ingredientsDropDown.grid(row=6, column=2, padx=0, pady=(0,10))

        ingredientsDropDown.bind("<<ComboboxSelected>>", dropdownIngredientSelectedFunc)

        amountLabel = Label(addMealFrame, text="Amount")
        amountLabel.grid(row=7, column=1, pady=(0,10))

        amountEntry = Entry(addMealFrame)
        amountEntry.grid(row=7, column=2, padx=0, pady=(0,10))

        addBtn = Button(addMealFrame, text="Add", command=lambda: addMealIngredientFunc())
        addBtn.grid(row=7, column=3, padx=10, pady=(0,10))

        queryLabel = Label(addMealFrame, text="")
        queryLabel.grid(row=8, column=2, padx=0, pady=(0,10))

        submitMealBtn = Button(addMealFrame, text="Submit Meal", command=lambda: submitMealBtnFunc())

        if statementType == 0:      #This if statement is used to change the text of the submit button depending on if
                                    #the window has been called for creating a new meal or for editing a meal
            submitMealBtn.config(text="Submit Meal")
        elif statementType == 1:
            submitMealBtn.config(text="Update Meal")
        
        submitMealBtn.grid(row=9, column=2, padx=10, pady=(0,10))

        guideGramsLabel = Label(addMealFrame, text="Grams guide\n\n1 pinch = 0.36g\n1 teaspoon = 4.2g\n1 dessert spoon = 10g\n"
                                + "1 tablespoon = 14.3\n1 apple medium = 100g\n1 aubergine = 270g\n1 bay leaf = 0.2g\n"
                                + "1 bell pepper = 120g\n1 bread roll = 68g\n1 bread slice = 38g\n1 carrot = 72g\n"
                                + "1 celery stick = 50g\n1 chicken breast = 150g\n1 chicken drumstick = 44g\n"
                                + "1 courgette = 200g\n1 egg = 50g\n1 fish fillet = 140g\n1 garlic clove = 6g\n"
                                + "1 inch ginger = 7.5g\n1 leek = 125g\n1 lettuce leaf = 10g\n1 mild chilli = 20g\n"
                                + "1 new potato = 45g\n1 okra = 12g\n1 onion medium = 110g\n1 plantain = 240g\n"
                                + "1 potato = 170g\n1 sausage = 67g\n1 scotch bonnet chilli = 10g\n1 shallot = 25g\n"
                                + "1 sprig of thyme = 0.65g\n1 spring onion = 15g\n1 stock cube dry = 10g\n"
                                + "1 stock cube liquid = 448ml\n1 sweet potato = 130g\n1 tomatoe = 100g\n"
                                + "1 tortilla = 30g", justify="left", anchor="w")
        guideGramsLabel.grid(row=0, column=0, rowspan=9, sticky="nw", padx=20, pady=(5,0))

        if currentMealName != None:
            mealEntryName.insert(0, str(currentMealName))

        if currentMealServings != None:
            numServingsEntry.insert(0, str(currentMealServings))

        if currentMealImgDir != None:
            imgDirEntry.insert(0, str(currentMealImgDir))

        if currentMealInstructions != None:
            instructionsText.insert(1.0, str(currentMealInstructions))

        if currentMealIngredientsNameArray != None:
            for z in range(0, len(currentMealIngredientsNameArray)):
                addIngredienToGuiFunc(str(currentMealIngredientsNameArray[z]), str(currentMealIngredientsGramsArray[z]))

        #scale widgets code-------------------------------------------------------------------------------------------------------
            
        ADD_MEAL_PREV_WIDTH = 0      #Used to store the windows width the last time it was resized
        ADD_MEAL_NEED_RESIZE = False    #Used to store a boolean value so that the resize function doesn't get run
                                        #mulitiple times due to both the screen changing size and the mouse entering
                                        #the screen having the potential to the ultimatly trigger the resize function

        def addMealWindowSizeChangeFunc(e):
            nonlocal ADD_MEAL_NEED_RESIZE

            resizeBool = addMealCheckaddMealResizeFunc() #Calls the function to see if the window width has changed

            if resizeBool == True:  #This if stement check if the addMealCheckaddMealResizeFunc has
                                    #returned True meaning that the widgets do need resizing
                if ADD_MEAL_NEED_RESIZE != True:    #Checks that the ADD_MEAL_NEED_RESIZE variable isn't already
                                                    #true as the mouse entering the screen could have
                                                    #already cause it to become true
                    ADD_MEAL_NEED_RESIZE = True

                #Used so that the widgets are resized after half a second if the
                #mouse hasn't already triggered a resize by entering the window
                newMealRoot.after(600, addMealResizeAfterTimeFunc)  

        def addMealResizeAfterTimeFunc():
            nonlocal ADD_MEAL_NEED_RESIZE

            #This if statment checks that the ADD_MEAL_NEED_RESIZE variable is still true as the resizing of the
            #widgets could have already been triggered by the mouse entering the scrollbar or canvas meaning that
            #the ADD_MEAL_NEED_RESIZE variable would thus be False as the widgets would no longer need resizing
            if ADD_MEAL_NEED_RESIZE == True: 
                addMealResizeFunc()    

        def addMealResizeFunc():        #This function is responsible for resizing
                                        #the widgets to the size of the window
            nonlocal ADD_MEAL_NEED_RESIZE   #Needed so that it can be set back to false after resizing the widgets
                                            #so that the widgets don't get unnecessarily scaled multiple times
            nonlocal queryLabelArray
            nonlocal removeIngredientBtnArray

            canvas_width = addMealCanvas.winfo_width()    #Stores the current width of the canvas
            scaleValue = (canvas_width / 760)
                
            size = canvas_width / 40    #Dividing the window widths by 40 gives a good menu font size

            #This array is used to temporarly store all the newMealGUI window permanant widgets
            tempAddMealWidgetArray = [mealNameLabel, mealEntryName, numServingsLabel, numServingsEntry, imgDirLabel, imgDirEntry,
                                      imgDirBtn, instructionsLabel, instructionsText, newIngredientBtn, ingredientLabel,
                                      ingredientsDropDown, amountLabel, amountEntry, addBtn, queryLabel, submitMealBtn,
                                      guideGramsLabel]

            #Used for adjusting the font size for all the widget in the newMealGUI windows for
            #the widgets that are always displayed but not the dynamicalled added widgets
            for widgetConfIndex in range(0, len(tempAddMealWidgetArray)):
                tempAddMealWidgetArray[widgetConfIndex].config(font=("Times New Roman", int(11 * scaleValue)))

            
            #Used for adjusting the padding for all the widget in the newMealGUI windows for the
            #widgets that are always displayed but not the dynamicalled added widgets
            for widgetGridIndex in range(0, len(tempAddMealWidgetArray)):
                if widgetGridIndex == 0 or widgetGridIndex == 2 or widgetGridIndex == 5:
                    tempAddMealWidgetArray[widgetGridIndex].grid(padx=(int(10 * scaleValue),0), pady=int(5 * scaleValue))
                elif widgetGridIndex == 1:
                    tempAddMealWidgetArray[widgetGridIndex].grid(pady=(int(5 * scaleValue),int(10 * scaleValue)))
                elif widgetGridIndex == 3:
                    tempAddMealWidgetArray[widgetGridIndex].grid(pady=int(5 * scaleValue))
                elif widgetGridIndex == 4 or widgetGridIndex == 6:
                    tempAddMealWidgetArray[widgetGridIndex].grid(padx=int(10 * scaleValue), pady=int(5 * scaleValue))
                elif (widgetGridIndex == 7 or widgetGridIndex == 10 or widgetGridIndex == 11 or widgetGridIndex == 12
                      or widgetGridIndex == 13 or widgetGridIndex == 14 or widgetGridIndex == 15 or widgetGridIndex ==16):
                    tempAddMealWidgetArray[widgetGridIndex].grid(pady=(0,int(10 * scaleValue)))
                elif widgetGridIndex == 8:
                    tempAddMealWidgetArray[widgetGridIndex].grid(padx=int(10 * scaleValue), pady=(0,int(5 * scaleValue)))
                elif widgetGridIndex == 9:
                    tempAddMealWidgetArray[widgetGridIndex].grid(padx=(int(120 * scaleValue),0))
                elif widgetGridIndex == 17:
                    tempAddMealWidgetArray[widgetGridIndex].grid(padx=int(20 * scaleValue), pady=(int(5 * scaleValue),0))

            for queryLabelIndex in range(0, len(queryLabelArray)):
                queryLabelArray[queryLabelIndex].config(font=("Times New Roman", int(11 * scaleValue)))

            for removeIngredientIndex in range(0, len(removeIngredientBtnArray)):
                removeIngredientBtnArray[removeIngredientIndex].config(font=("Times New Roman", int(11 * scaleValue))) 
            

            #Updates the Bbox for the scrollbar after a small time delay so that the changes in
            #widgets dimensions have time to be implimented before the Bbox is updated 
            newMealRoot.after(200, addMeaIUpdateBbox)
            ADD_MEAL_NEED_RESIZE = False

        #Checks the windows previous known width with the current known width
        #so that the widgets arn't resized when they don't need to be
        def addMealCheckaddMealResizeFunc():
            nonlocal ADD_MEAL_PREV_WIDTH
            canvas_width = int(addMealCanvas.winfo_width())    #Stores the current width of the canvas
            
            if canvas_width > 1:
                if ADD_MEAL_PREV_WIDTH != canvas_width:
                    ADD_MEAL_PREV_WIDTH = canvas_width      #Save the canvas width to the
                                                            #ADD_MEAL_PREV_WIDTH variable
                    return True

        #This function is triggered whenever the mouse enters the canvas or scrollbar
        def addMealMouseEnterFunc(e):
            nonlocal ADD_MEAL_NEED_RESIZE

            if ADD_MEAL_NEED_RESIZE == True:
                addMealResizeFunc()

        def addMealMouseWheelScrolled(e):      #This function is triggered whenever the mouse wheel is scrolled
            sliderLocation = addMealScrollbar.get()      #Gets the top and bottom locations of the scroll bars slider

            #This if stops the yview from been scrolled when the slider isn't visible on the scrollbar 
            if sliderLocation[0] != 0.0 or sliderLocation[1] != 1.0:
                addMealCanvas.yview_scroll(int(-1*(e.delta/120)), "units")
        #-------------------------------------------------------------------------------------------------------------------------


        #Event binding code-------------------------------------------------------------------------------------------------------
                
        #Bind the apps configuration so that screen size chnages can be detected

        #Event that is triggered when windows changes size
        newMealRoot.bind("<Configure>", addMealWindowSizeChangeFunc)
        #Event that is triggered when the mouse enters the canvas
        addMealCanvas.bind("<Enter>", addMealMouseEnterFunc)
        #Event that is triggered when the mouse enters the scrollbar
        addMealScrollbar.bind("<Enter>", addMealMouseEnterFunc) 

        #Event that is triggered when the mouse wheel is scrolled
        newMealRoot.bind("<MouseWheel>", addMealMouseWheelScrolled)     
        #-------------------------------------------------------------------------------------------------------------------------

        def rootCloseFunc():        #This function is called when the close button is clicked on the window
            global newMealWinOpen
            global addMealCurrentRoot
            
            print("Window closed")
            newMealWinOpen = False
            addMealCurrentRoot = None
            newMealRoot.destroy()      #Used to detroy the newMealRoot window when the close button is clicked
            
        #Event that is triggered when the close button is clicked on the newMealRoot window 
        newMealRoot.protocol("WM_DELETE_WINDOW", rootCloseFunc)        
        
        newMealRoot.mainloop()
    else:       #This will run if the window already exists
        if addMealCurrentRoot.state() == "iconic":     #Checks if the window exists but has been minised
            addMealCurrentRoot.deiconify()     #Unminises the window

#---------------------------------------------------------------------------------------------------------------------------------

#menuFrame code ------------------------------------------------------------------------------------------------------------------

def hidePageFunc():     #This function hides all the child frames of the canvasParentFrame except the menuFrame
    for widget in canvasParentFrame.winfo_children():   #This for statemnt iterates through all the child
                                                        #frames in the canvasParentFrame
        if str(widget) != ".!frame.!canvas.!frame.!frame":      #Checks that the frame isnt the menuFrame
            widget.grid_forget()

#This function is responsible for placing the correct childFrame onto the canvas and calling
#the correct functions to remove the other childFrame from the canvas and to resize the widgets
def changeChildFrameFunc():
    global CURRENT_CHILD_FRAME

    hidePageFunc()
    #This line places the new childFrame onto the grid in the canvasParentFrame grid
    childFrameArray[CURRENT_CHILD_FRAME - 1].grid(row=1, column=0, sticky="nesw")
    resizeFunc()    #Called so that all the widgets in the newly added
                    #frame are scalled correctly to the window

def changeMenuFunc():
    for i in range (0, len(menuBtnArray)):
            menuBtnArray[i].grid_forget()

    if CURRENT_CHILD_FRAME == 4:    #Adds the back button for the meal info page that
                                    #when clicked will take a user back to the meals page
        mealMenuBtn1.grid(row=0, column=0, sticky="w")
        mealMenuBtn2.grid(row=0, column=1, sticky="ew")
        mealMenuBtn3.grid(row=0, column=2, sticky="e")
    elif CURRENT_CHILD_FRAME == 5:  #Adds the back button for the date info page that when
                                    #clicked will take a user back to the calendar page
        calendarMenuBtn1.grid(row=0, column=0, sticky="w")

def changeBackMenuMealFunc():       #This function updates the menu frame when changing
                                    #back from the meal info page back to the meals page
    mealMenuBtn1.grid_forget()
    mealMenuBtn2.grid_forget()
    mealMenuBtn3.grid_forget()

    menuBtn1.grid(row=0, column=0)
    menuBtn2.grid(row=0, column=1)
    menuBtn3.grid(row=0, column=2)

    hidePageFunc()
    #This line places the new childFrame onto the grid in the canvasParentFrame grid
    childFrameArray[CURRENT_CHILD_FRAME - 1].grid(row=1, column=0, sticky="nesw")

    resizeFunc()

#This function updates the menu frame when changing back from the day details page back to the calendar page
def changeBackMenuCalendarFunc():       
    calendarMenuBtn1.grid_forget()

    menuBtn1.grid(row=0, column=0)
    menuBtn2.grid(row=0, column=1)
    menuBtn3.grid(row=0, column=2)

    hidePageFunc()
    #This line places the new childFrame onto the grid in the canvasParentFrame grid
    childFrameArray[CURRENT_CHILD_FRAME - 1].grid(row=1, column=0, sticky="nesw")

    resizeFunc()

def updateCalendarDateBtns():
    pg1DateLabelArray = (pg1DateLabel.cget("text")).split("/")

    pg1TempMonth = int(pg1DateLabelArray[0])
    pg1TempYear = int(pg1DateLabelArray[1])

    maxDays = calNumDaysForMonthFunc(pg1TempMonth, pg1TempYear)

    #Calls the method responsible for putting the text into the calendar page date buttons
    populateCalendarPageBtnsFunc(maxDays)

#Click functions for the menu buttons

def clickBtn1Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 1:
        CURRENT_CHILD_FRAME = 1   #Set so that the correct button can be underlined in the menu
        changeChildFrameFunc()
        updateCalendarDateBtns()    #Updates the calendar page buttons

def clickBtn2Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 2:
        CURRENT_CHILD_FRAME = 2   #Set so that the correct button can be underlined in the menu
        changeChildFrameFunc()

def clickBtn3Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 3:
        CURRENT_CHILD_FRAME = 3   #Set so that the correct button can be underlined in the menu
        changeChildFrameFunc()
        populateWeeksFunc()     #Calls the function that inserts all the values into each week

def clickBtn4Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 2:
        CURRENT_CHILD_FRAME = 2   #Set so that the correct button can be underlined in the menu
        changeBackMenuMealFunc()

def clickBtn5Func():
    mealNameFromLabel = mealNameLabel.cget("text")      #Gets the name of the meal from the meals name label

    #Reads all the values from the meals table using the name of the name that was in the name label
    result = readDBQuery('SELECT * FROM meals WHERE name = "' + str(mealNameFromLabel) + '";')

    mealInstructionsText = str(result[0][3])    #Reads the meals instructions from the query result
    #Replaces the # with \n so that the instructions has the correct line
    #breaks when displayed in the insructions box of the window
    mealInstructionsText = mealInstructionsText.replace("^", "\n")

    #Reads all of the ingredient values that are in the meal_ingredients array for the given meal
    ingredientsResult = readDBQuery('SELECT ingredient_id, grams_amount FROM meal_ingredients WHERE meal_id = "'
                                    + str(result[0][0]) + '";')    

    tempMealIngredientsGrams = []       #Used to store the grams amount for the meals ingredients so
                                        #that they can be passed in to the createMealGuiFunc
    tempMealIngredientsName = []        #Used to store the ingredients name for the meals ingredients
                                        #so that they can be passed in to the createMealGuiFunc

    for x in range(0, len(ingredientsResult)):
        #Gets the name of the ingredient using its id value in the ingredientsResult
        ingredientName = readDBQuery('SELECT name FROM ingredients WHERE id = "' + str(ingredientsResult[x][0]) + '";')     
        tempMealIngredientsGrams.append(str(ingredientsResult[x][1]))
        tempMealIngredientsName.append(ingredientName[0][0])

    #Calles the functiont that creates the add new / edit meal window, passing 1 to tell it that it
    #should be the edit window, passing the meals name, number of servings, instructions for the
    #meal, meal image directory, array of the meals ingredients names, array of the meals
    #ingredients grams amounts
    createMealGuiFunc(1,str(result[0][1]),str(result[0][2]),mealInstructionsText,str(result[0][4]),
                      tempMealIngredientsName, tempMealIngredientsGrams)  

def clickBtn6Func():
    global imageBtnsArray
    global tickBtnArray
    global imgBtnEntryBoxArray

    #Gets the name of the meal from the meals name label
    mealNameFromLabel = mealNameLabel.cget("text")

    #Used to get the meal id of the meal using its name
    result = readDBQuery('SELECT id FROM meals WHERE name = "' + str(mealNameFromLabel) + '";') 
    
    answer = askyesno(title="Delete Meal?", message="Are you sure that you want to delete the meal?")

    if answer == True:  
        print("Delete meal")
        writeDBQuery('DELETE FROM meal_plan WHERE meal_id = ' + str(result[0][0]) + ';')
        writeDBQuery('DELETE FROM meal_nutrition WHERE meal_id = ' + str(result[0][0]) + ';')
        writeDBQuery('DELETE FROM meal_ingredients WHERE meal_id = ' + str(result[0][0]) + ';')
        writeDBQuery('DELETE FROM meals WHERE id = ' + str(result[0][0]) + ';')
        

        #This for statemnt iterates through all the child frames in the canvasParentFrame
        for widget in childFrame2.winfo_children(): 
            if (str(widget) != ".!frame.!canvas.!frame.!frame3.!button" and str(widget) != ".!frame.!canvas.!frame.!frame3.!label"
                and str(widget) != ".!frame.!canvas.!frame.!frame3.!button2"
                and str(widget) != ".!frame.!canvas.!frame.!frame3.!button3"
                and str(widget) != ".!frame.!canvas.!frame.!frame3.!button4"
                and str(widget) != ".!frame.!canvas.!frame.!frame3.!button5"):      #Checks that the frame isnt the menuFrame
                widget.grid_forget()

        #This section clears all the arrays that are used for displaying meals on the meals page
        tickBtnArray.clear()
        imgBtnEntryBoxArray.clear()
        imageBtnsArray.clear()
        mealImagesArray.clear()
        mealNameArray.clear()

        clickBtn4Func()     #Changes the frame back to the meals page

        #Calls the functions that are responsible for populating the arrays that we're cleared above
        loadDataMealPgFunc()
        imgBtnCreateImageFunc()
        createInitialTickEntryFunc()

        #Class the function that adds the meals onto the meals page
        placeMealBtnsFunc()

        resizeFunc()
    elif answer == False:
        print("Don't delete meal")

def clickBtn7Func():
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME != 1:
        CURRENT_CHILD_FRAME = 1   #Set so that the correct button can be underlined in the menu

        for i in range(0, len(calendarDayDetailsName)):
            calendarDayDetailsName[i].grid_remove()
            #calendarDayDetailsName[i].destroy()

        for x in range(0, len(calendarDayDetailsInfo)):
            calendarDayDetailsInfo[x].grid_remove()
            #calendarDayDetailsInfo[x].destroy()

        calendarDayDetailsName.clear()
        calendarDayDetailsInfo.clear()
        
        changeBackMenuCalendarFunc()


#Sets the weight for the menuFrame grid
menuFrame.rowconfigure(index=0, weight=1)
menuFrame.columnconfigure(index=0, weight=1)
menuFrame.columnconfigure(index=1, weight=1)
menuFrame.columnconfigure(index=2, weight=1)

#Create menu buttons
#Borderwidth removes the buttons style
menuBtn1 = Button(menuFrame, text="Calendar", command=clickBtn1Func, borderwidth=0)     
menuBtn2 = Button(menuFrame, text="Meals", command=clickBtn2Func, borderwidth=0)
menuBtn3 = Button(menuFrame, text="Analytics", command=clickBtn3Func, borderwidth=0)

#Back button that is used in the menu bar on the page that shows information about the individal meal
mealMenuBtn1 = Button(menuFrame, text="< Back", command=clickBtn4Func, borderwidth=0)
mealMenuBtn2 = Button(menuFrame, text="Edit Meal", command=clickBtn5Func, borderwidth=0)
mealMenuBtn3 = Button(menuFrame, text="Delete Meal", command=clickBtn6Func, borderwidth=0)

#Back button that is used in the menu bar on that page
#that shows the meals for the given day on the calender page
calendarMenuBtn1 = Button(menuFrame, text="< Back", command=clickBtn7Func, borderwidth=0)

menuBtnArray = [menuBtn1, menuBtn2, menuBtn3]

#Adds the menu buttons to the menuFrame's grid
menuBtn1.grid(row=0, column=0)
menuBtn2.grid(row=0, column=1)
menuBtn3.grid(row=0, column=2)


#---------------------------------------------------------------------------------------------------------------------------------



#Used to get the current date in a format that has a 4 digit year
today = (date.today()).strftime("%m/%d/%Y")     
todaySplit = today.split("/")
today = str(todaySplit[1]) + "/" + str(todaySplit[0]) + "/" + str(todaySplit[2])

def calSubmitBtnFunc(calWindow, cal):
    tempDate = cal.get_date()
    tempDateSplit = tempDate.split("/")

    if int(tempDateSplit[0]) < 10:  #Month
        todaySplit[0] = "0" + str(tempDateSplit[0])
    else:
        todaySplit[0] = tempDateSplit[0]

    if int(tempDateSplit[1]) < 10:  #Day
        todaySplit[1] = "0" + str(tempDateSplit[1])
    else:
        todaySplit[1] = tempDateSplit[1]
        
    todaySplit[2] = (cal.get_displayed_month())[1]    #Year

    #Sets the year from the calendar in a 4 digit format
    selectedDate = str(todaySplit[1]) + "/" + str(todaySplit[0]) + "/" + str(todaySplit[2])

    dateLabel.config(text= selectedDate)
    calWindow.destroy()     #Destroys the calendar window

def openCalendarFunc():
    calWindow = Toplevel(root)
    #calWindow.geometry("400x250")
    calWindow.title("Calendar")
    calWindow.iconbitmap(programImagesDir + r"images\calendar_icon.ico")
    calWindow.rowconfigure(0, weight=1)
    calWindow.columnconfigure(0, weight=1)

    calWindow.minsize(222, 220)

    cal = Calendar(calWindow, selectmode="day", year=int(todaySplit[2]), month=int(todaySplit[0]), day=int(todaySplit[1]))
    cal.grid(row= 0, column= 0, sticky="NESW")

    calSubmitBtn = Button(calWindow, text="Submit", command= lambda: calSubmitBtnFunc(calWindow, cal))
    calSubmitBtn.grid(row= 1, column= 0, padx= 5, pady =5, sticky="NESW")
    calSubmitBtn.config(font=("Times New Roman", 20))

def calNumDaysForMonthFunc(month, year):
    maxDays = 0
    
    if month == 4 or month == 6 or month == 9 or month == 11:
        maxDays = 30
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        maxDays = 31
    else:
        if (year / 4).is_integer() == True:
            maxDays = 29
        else:
            maxDays = 28
    return maxDays

def formatDateFunc(day, month):
    dayStr = ""
    monthStr = ""

    if day < 10:        #Makes single digit dates into 2 digit dates
        dayStr = "0" + str(day)
    else:
        dayStr = str(day)

    if month < 10:      #Makes single digit months into 2 digit months
        monthStr = "0" + str(month)
    else:
        monthStr = str(month)

    return dayStr, monthStr

def updateDateLabelFunc(day, month, year):
    todaySplit[1] = day
    todaySplit[0] = month
    todaySplit[2] = year

    dayStr, monthStr = formatDateFunc(day, month)

    yearStr = str(year)
    
    dateLabel.config(text=(dayStr + "/" + monthStr + "/" + yearStr))

def updateTickEntryBtnSateFunc():       #This function is responsible for updating the tick button and entry
                                        #box of each meal depending on if the meal is in the meal_plan
                                        #table for the given date
    savedMeals, amountMeals, null = readMealPlanFunc()

    for i in range (0, len(imageBtnsArray)):
        try:
            savedMeals.remove(str(i + 1))   #Removes the meal from the savedMeals array if it is
                                            #already in the meal_plan table for that date
            tickBtnArray[i].config(image= scaled_tick_img2, text= "1")
            entryText = str(amountMeals[0])
            imgBtnEntryBoxArray[i].delete(0, "end")
            imgBtnEntryBoxArray[i].insert(0, str(amountMeals[0]))
            amountMeals = amountMeals[1:]
        except ValueError as e:
            tickBtnArray[i].config(image= scaled_tick_img1, text= "0")
            imgBtnEntryBoxArray[i].delete(0, "end")
            imgBtnEntryBoxArray[i].insert(0, "1")
  

def rightArrowBtnFunc():    #Called when the right arrow is clicked so that the day can be increased by 1
    day = int(todaySplit[1])
    month = int(todaySplit[0])
    year = int(todaySplit[2])

    maxDays = calNumDaysForMonthFunc(month, year)


    day = day + 1

    if day > maxDays:       #Stops the number of days from been too large for the month
        day = 1
        month = month + 1

    if month > 12:      #Stops the month from been too large
        month = 1
        year = year + 1


    updateDateLabelFunc(day, month, year)
    updateTickEntryBtnSateFunc()

def leftArrowBtnFunc():     #Called when the left arrow is clicked so that the day can be decreased by 1
    day = int(todaySplit[1])
    month = int(todaySplit[0])
    year = int(todaySplit[2])

    day = day - 1

    if day < 1:     #Stops the day from been less than 1
        passMonth = 0

        if (month - 1) < 1:
            passMonth = 12
        else:
            passMonth = (month - 1)
        
        maxDays = calNumDaysForMonthFunc(passMonth, year)
        day = maxDays
        month = month - 1

    if month < 1:       #Stops the month from been less than 1
        month = 12
        year = year - 1

    updateDateLabelFunc(day, month, year)
    updateTickEntryBtnSateFunc()

#ChildFrame1 code ----------------------------------------------------------------------------------------------------------------

calendarPageBtnArray = []

def hideCalendarPageBtnsFunc(maxDays):
    if maxDays == 31:
        if calendarPageBtnArray[-1].winfo_viewable() == 0:      #Checks if the 31st button is visible
            calendarPageBtnArray[-1].grid(row=5, column = 2, padx=7, pady=10)
        
        if calendarPageBtnArray[-2].winfo_viewable() == 0:      #Checks if the 30th button is visible
            calendarPageBtnArray[-2].grid(row=5, column = 1, padx=7, pady=10)

        if calendarPageBtnArray[-3].winfo_viewable() == 0:      #Checks if the 29th button is visible
            calendarPageBtnArray[-3].grid(row=5, column = 0, padx=7, pady=10)

    if maxDays == 30:
        calendarPageBtnArray[-1].grid_forget()      #Hides the 31st button

        if calendarPageBtnArray[-2].winfo_viewable() == 0:      #Checks if the 30th button is visible
            calendarPageBtnArray[-2].grid(row=5, column = 1, padx=7, pady=10)

        if calendarPageBtnArray[-3].winfo_viewable() == 0:      #Checks if the 29th button is visible
            calendarPageBtnArray[-3].grid(row=5, column = 0, padx=7, pady=10)

    elif maxDays == 29:
        calendarPageBtnArray[-1].grid_forget()      #Hides the 31st button
        calendarPageBtnArray[-2].grid_forget()      #Hides the 30th button 

        if calendarPageBtnArray[-3].winfo_viewable() == 0:      #Checks if the 29th button is visible
            calendarPageBtnArray[-3].grid(row=5, column = 0, padx=7, pady=10)
    elif maxDays == 28:
        calendarPageBtnArray[-1].grid_forget()  #Hides the 31st button
        calendarPageBtnArray[-2].grid_forget()  #Hides the 30th button
        calendarPageBtnArray[-3].grid_forget()  #Hides the 29th button

#This function calculates the nutritional values per serving for the meal of the given mealID
def mealNutritionValuesFunc(mealID):        
    #Used to get all the ingredients and gram amount for the meal
    gramsID = readDBQuery('SELECT ingredient_id, grams_amount FROM meal_ingredients WHERE meal_id = ' + str(mealID))

    #Retrives the number of servings for the meal
    numServings = readDBQuery('SELECT num_servings FROM meals WHERE id = ' + str(mealID))   

    #This array is used to store the total nutritional values for the meal
    mealValuesTotalArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]    

    #This for loop is responsible for calculating the calorie amouts for each ingredient and adding it to the total for the meal
    for x in range(0, len(gramsID)):
        mealValues = readDBQuery('SELECT energy, fat, sat_fat, carbs, sugar, fibre, protein, salt, vit_a, thiamin, riboflavin,'
                                 + 'niacin, vit_b6, vit_b12, vit_c, vit_d, calcium, phosphorus, magnesium, potassium,'
                                 + 'iron, zinc, copper, selenium FROM ingredients WHERE id = ' + str(gramsID[x][0]))
                                #Selects the calories amount per 100g for the specified ingredient
        mealValuesArray = []
            

        for n in range(0, len(mealValues[0])):
            if mealValues[0][n] == None:      #If the value is None then it will get changed to 0
                mealValuesArray.append(0)
            else:
                mealValuesArray.append(mealValues[0][n])


        for y in range(0, len(mealValues[0])):      #Adds the nutrient/vitamin value of each ingredinet to the array
            mealValuesTotalArray[y] = (mealValuesTotalArray[y] +
                                       ((int((gramsID[x][1] / 100) * mealValuesArray[y])) / numServings[0][0]))
                

    for k in range(0, len(mealValuesTotalArray)):       #Removes .0 from the end of number e.g. 0.0 becomes 0 or 50.0 becomes 50
        temp = str(mealValuesTotalArray[k]).split(".")

        if temp[1] == "0":      #Checks if the number after the . is only a zero
            mealValuesTotalArray[k] = int(temp[0])

    return mealValuesTotalArray

#This function writes the nutritional values that we're calculated to the meal_nutrition table
def calMealNutritionalInfoFunc(mealID): 
    mealValuesTotalArray = mealNutritionValuesFunc(mealID)
    
    add_meal_nutrition_query = """
            INSERT INTO meal_nutrition(meal_id, energy, fat, sat_fat, carbs, sugar, fibre, protein, salt,
            vit_a, thiamin, riboflavin, niacin, vit_b6, vit_b12, vit_c, vit_d, calcium, phosphorus, magnesium,
            potassium, iron, zinc, copper, selenium)
            VALUES
            (
            """
    add_meal_nutrition_query = (add_meal_nutrition_query + str(mealID) + ', ' + str(mealValuesTotalArray[0]) + ', '
    + str(mealValuesTotalArray[1]) + ', ' + str(mealValuesTotalArray[2]) + ', ' + str(mealValuesTotalArray[3]) + ', '
    + str(mealValuesTotalArray[4]) + ', ' + str(mealValuesTotalArray[5]) + ', ' + str(mealValuesTotalArray[6]) + ', '
    + str(mealValuesTotalArray[7]) + ', ' + str(mealValuesTotalArray[8]) + ', ' + str(mealValuesTotalArray[9]) + ', '
    + str(mealValuesTotalArray[10]) + ', ' + str(mealValuesTotalArray[11]) + ', ' + str(mealValuesTotalArray[12]) + ', '
    + str(mealValuesTotalArray[13]) + ', ' + str(mealValuesTotalArray[14]) + ', ' + str(mealValuesTotalArray[15]) + ', '
    + str(mealValuesTotalArray[16]) + ', ' + str(mealValuesTotalArray[17]) + ', ' + str(mealValuesTotalArray[18]) + ', '
    + str(mealValuesTotalArray[19]) + ', ' + str(mealValuesTotalArray[20]) + ', ' + str(mealValuesTotalArray[21]) + ', '
    + str(mealValuesTotalArray[22]) + ', ' + str(mealValuesTotalArray[23]) + ");")
    writeDBQuery(add_meal_nutrition_query)  #Adds the nutritional information per portion to the meal_nutrition table


#This function reads the nutritional values for the given meal id, from the meal_nutrition table
def readMealNutritionFunc(mealID):      
    mealValuesArray =[]
    mealValuesResult = readDBQuery('SELECT energy, fat, sat_fat, carbs, sugar, fibre, protein, salt, vit_a, thiamin,'
                                   + 'riboflavin, niacin, vit_b6, vit_b12, vit_c, vit_d, calcium, phosphorus, magnesium,'
                                   + 'potassium, iron, zinc, copper,selenium FROM meal_nutrition WHERE meal_id = ' + str(mealID))

    for x in range(0, len(mealValuesResult[0])):
        mealValuesArray.append(mealValuesResult[0][x])

    return mealValuesArray

def populateCalendarPageBtnsFunc(maxDays):
    splitDateText = (pg1DateLabel.cget("text")).split("/")
    suffix = ""

    for z in range (0, maxDays):
        #Selects all the meals in the database for that given date
        result = readDBQuery('SELECT meal_id, amount FROM meal_plan WHERE meal_date = "' + str(splitDateText[1])
                             + "-" + str(splitDateText[0]) + "-" + str(z + 1) + '"')    
        numMeals = 0

        totalCalsForDay = 0
        for n in range (0, len(result)):
            mealID = str(result[n][0])
            mealAmount = int(result[n][1])
            numMeals = numMeals + mealAmount

            #Reads the kcals per portion from the meal_nutrition table
            kcalResult = readDBQuery('SELECT energy FROM meal_nutrition WHERE meal_id = ' + str(mealID))        

            #Adds the total nutritional values of one serving of the meal onto the total taking
            #into account that the same meal can be eaten more than once on the same day
            for x in range (0, mealAmount): 
                totalCalsForDay = totalCalsForDay + int(kcalResult[0][0])
            
        
        if (z + 1) == 1 or (z + 1) == 21 or (z + 1) ==31:   #This if statments are responsible for decidings the
                                                            #siffix's used on the calendar date buttons
            suffix = "st"
        elif (z + 1) == 3 or (z + 1) == 23:
            suffix = "rd"
        elif (z + 1) == 2 or (z + 1) == 22:
            suffix = "nd"
        else:
            suffix = "th"

        #This is statement changes the background colour depending on the number of meals added to the plan for the given day
        if numMeals == 0:
            #Adds the text to the calendar date button
            calendarPageBtnArray[z].config(text=str(z + 1) + suffix + "\nNumber of meals = " + str(numMeals)
                                           + "\nTotal kcals = " + str(int(totalCalsForDay)) + "kcals", bg="#f0f0f0")
        elif numMeals == 1:
            #Adds the text to the calendar date button
            calendarPageBtnArray[z].config(text=str(z + 1) + suffix + "\nNumber of meals = " + str(numMeals)
                                           + "\nTotal kcals = " + str(int(totalCalsForDay)) + "kcals", bg="#f1fcbd")
        elif numMeals == 2:
            #Adds the text to the calendar date button
            calendarPageBtnArray[z].config(text=str(z + 1) + suffix + "\nNumber of meals = " + str(numMeals)
                                           + "\nTotal kcals = " + str(int(totalCalsForDay)) + "kcals", bg="#b7ffa1")
        elif numMeals > 2:
            #Adds the text to the calendar date button
            calendarPageBtnArray[z].config(text=str(z + 1) + suffix + "\nNumber of meals = " + str(numMeals)
                                           + "\nTotal kcals = " + str(int(totalCalsForDay)) + "kcals", bg="#79fc58")  

def placeCalendarPageBtnFunc():
    x = 0 #x is used for the starting column number
    n = 1 #n is used for the starting row number
    for i in range (0, len(calendarPageBtnArray)):
        if x == 7:      #The value in this if statment is set to the number of columns that you want
            x = 0
            n = n + 1

        calendarPageBtnArray[i].grid(row=n, column=x, padx=7, pady=10)     #Places the meal image button into the grid
        x = x + 1

calendarDayDetailsName = []     #This array is used to store all the meal name labels that are added to childFrame5
calendarDayDetailsInfo = []     #This array is used to store all the labels that are used to display the
                                #meals nutritional information that are added to childFrame5

#This function is responsible for creating and adding to childFrame5 the labels that display
#the nutritional information of each meal when a day is clicked on the calendar page
def createMealInfoLabel(mealName, infoStringArray, indexValue):      
    rowVal = (2 * (indexValue + 1))     #Used to calculate the row that the mean information label should be on

    #This label is for the name of the meal
    mealInfoNameLabel = Label(childFrame5, text=mealName, justify="left", anchor="w", width = 44)   
    calendarDayDetailsName.append(mealInfoNameLabel)

    #This if statement adds the mealNameLabel to the grid an add the y padding between
    #the meals with the first meal having no y padding as it is the first
    if (rowVal - 1) == 1:   
        mealInfoNameLabel.grid(row=(rowVal - 1), column=0, columnspan=4, padx=10, pady=0, sticky="w")
    else:
        mealInfoNameLabel.grid(row=(rowVal - 1), column=0, columnspan=4, padx=10, pady=(30,0), sticky="w")

    #This for loop creates and adds the meals nutritional information in the row below
    #the meals name using 4 seperate labels as there are 4 columns of nutritional information
    for i in range(0, len(infoStringArray)):
        mealInfoLabel = Label(childFrame5, text=infoStringArray[i], justify="left", anchor="w", width=20)
        calendarDayDetailsInfo.append(mealInfoLabel)
        mealInfoLabel.grid(row=rowVal, column=i, padx=(10,2), sticky="w")
    

#This function is responsible providing all the meals for the date to the function that reads the nutritional information for
#each meal, the function is required to populate childFrame5 with the correct information whilst also changing the child
#frame to childFrame5
def individualMealNutritionalInfoFunc(mealIDAmount, date):  
    global CURRENT_CHILD_FRAME  
    mealForDateID = []

    for i in range(0, len(mealIDAmount)):       #Used to add all the meal ids to the mealForDateID array taking into account
                                                #the amount, so the id will be added to the array equal to the amount value
        for n in range(0, int(mealIDAmount[i][1])):
            mealForDateID.append(mealIDAmount[i][0])

    mealValuesStringArray = []
    prevMealID = 0
    mealName = ""
    for z in range(0, len(mealForDateID)):
        if prevMealID != int(mealForDateID[z]):     #Checks that the meal isn't the same as the meal that was previously
                                                    #added as if it is then new nutritional values dont need to be read
            mealName = readDBQuery('SELECT name FROM meals WHERE id = ' + str(mealForDateID[z]))        #Gets the name of the meal
            mealValuesTotalArray = readMealNutritionFunc(mealForDateID[z])      #Calls the function that reads the
                                                                                #nutritional values of the meal

            mealValuesStringArray = ["Calories = " + str(int(mealValuesTotalArray[0])) + "Kcals\n" +
                                     "Fat = " + str(mealValuesTotalArray[1]) + "g\n" +
                                     "Saturated Fat = " + str(mealValuesTotalArray[2]) + "g\n" +
                                     "Carbohydrates = " + str(mealValuesTotalArray[3]) + "g\n" +
                                     "Sugar = " + str(mealValuesTotalArray[4]) + "g\n" +
                                     "Fibre = " + str(mealValuesTotalArray[5]) + "g",
                                     "Protein = " + str(mealValuesTotalArray[6]) + "g\n" +
                                     "Salt = " + str(mealValuesTotalArray[7]) + "g\n" +
                                     "Vitamin A = " + str(mealValuesTotalArray[8]) + "μg\n" +
                                     "Thiamin = " + str(mealValuesTotalArray[9]) + "mg\n" +
                                     "Riboflavin = " + str(mealValuesTotalArray[10]) + "mg\n" +
                                     "Niacin = " + str(mealValuesTotalArray[11]) + "mg",
                                     "Vitamin B6 = " + str(mealValuesTotalArray[12]) + "mg\n" +
                                     "Vitamin B12 = " + str(mealValuesTotalArray[13]) + "μg\n" +
                                     "Vitamin C = " + str(mealValuesTotalArray[14]) + "mg\n" +
                                     "Vitamin D = " + str(mealValuesTotalArray[15]) + "μg\n" +
                                     "Calcium = " + str(mealValuesTotalArray[16]) + "mg\n" +
                                     "Phosphorus = " + str(mealValuesTotalArray[17]) + "mg",
                                     "Magnesium = " + str(mealValuesTotalArray[18]) + "mg\n" +
                                     "Potassium = " + str(mealValuesTotalArray[19]) + "mg\n" +
                                     "Iron = " + str(mealValuesTotalArray[20]) + "mg\n" +
                                     "Zinc = " + str(mealValuesTotalArray[21]) + "mg\n" +
                                     "Copper = " + str(mealValuesTotalArray[22]) + "mg\n" +
                                     "Selenium = " + str(mealValuesTotalArray[23]) + "μg"]

        createMealInfoLabel(mealName[0][0], mealValuesStringArray, z)       #Calls the function that creates the label
                                                                            #for the meal and adds it to childFrame5
        prevMealID = int(mealForDateID[z])
        
    if CURRENT_CHILD_FRAME != 5:        #Checks that the current child frame been displayed isn't 5
        CURRENT_CHILD_FRAME = 5         #Sets the CURRENT_CHILD_FRAME to 5 so that childFrame5 will be displayed

        changeMenuFunc()        #Calls the function responsible for removing the default options from the
                                #menu frame and replaces it with a back option
        changeChildFrameFunc()  #Calls the function that changes the child frame to the child
                                #frame number that is stored in CURRENT_CHILD_FRAME

        

#This function is responsible for retrieving the meals that are in the plan for the specified day
def calendarPageBtnClickedFunc(calendarBtnObj): 
    pg1DateLabelArray = (pg1DateLabel.cget("text")).split("/")      #Gets the month and year from the label on the calendar page
    day = (((str(calendarBtnObj.cget("text"))).split("\n"))[0])[:-2]        #Gets the day of the month from the button

    if len(day) == 1:
        day = "0" + day
        
    date = pg1DateLabelArray[1] + "-" + pg1DateLabelArray[0] + "-" + day

    #Retuns an array of all the meal_ids and amounts for the meals on the specifed date
    mealIDAmount = readDBQuery('SELECT meal_id, amount FROM meal_plan WHERE meal_date = "' + date + '"')

    individualMealNutritionalInfoFunc(mealIDAmount ,date)       #Calls the finction that calculates the meals nutritional values
    

    

def createCalendarPageBtnsFunc():       #This function creates the date buttons on the calendar page
    tempCalPg1Btn = Button(childFrame1, borderwidth=3, width=17, height=4, font=("Times New Roman", 19), justify="left",
                           anchor="nw", command= lambda: calendarPageBtnClickedFunc(tempCalPg1Btn))
    calendarPageBtnArray.append(tempCalPg1Btn)

def createNumCalenderPageBtnsFunc(maxDays):
    for z in range (0, maxDays):
        #Creating the button needs to be in its own function so that each button is assign its individual click binding
        createCalendarPageBtnsFunc()
    placeCalendarPageBtnFunc()


        

def pg1LeftArrowBtnFunc():
    pg1DateLabelArray = (pg1DateLabel.cget("text")).split("/")

    pg1TempMonth = int(pg1DateLabelArray[0])
    pg1TempYear = int(pg1DateLabelArray[1])

    pg1TempMonth = pg1TempMonth - 1     #Decreases the month by 1

    if pg1TempMonth < 1:
        pg1TempMonth = 12
        pg1TempYear = pg1TempYear - 1 #Decreases the year by 1

    maxDays = calNumDaysForMonthFunc(pg1TempMonth, pg1TempYear)

    pg1TempDay, pg1TempMonth = formatDateFunc(0, pg1TempMonth)

    pg1DateLabel.config(text=str(pg1TempMonth) + "/" + str(pg1TempYear))

    hideCalendarPageBtnsFunc(maxDays)       #Called to update the calendar date buttons that are visibile
    updateCalendarDateBtns()    #Updates the calendar page buttons

def pg1RightArrowBtnFunc():
    pg1DateLabelArray = (pg1DateLabel.cget("text")).split("/")

    pg1TempMonth = int(pg1DateLabelArray[0])
    pg1TempYear = int(pg1DateLabelArray[1])

    pg1TempMonth = pg1TempMonth + 1     #Increases the month by 1

    if pg1TempMonth > 12:
        pg1TempMonth = 1
        pg1TempYear = pg1TempYear + 1 #Increases the year by 1

    maxDays = calNumDaysForMonthFunc(pg1TempMonth, pg1TempYear)

    pg1TempDay, pg1TempMonth = formatDateFunc(0, pg1TempMonth)

    pg1DateLabel.config(text=str(pg1TempMonth) + "/" + str(pg1TempYear))

    hideCalendarPageBtnsFunc(maxDays)       #Called to update the calendar date buttons that are visibile
    updateCalendarDateBtns()    #Updates the calendar page buttons
       

pg1LeftArrowBtn = Button(childFrame1, text="<", command=pg1LeftArrowBtnFunc)    #Date selection left arrow
pg1LeftArrowBtn.grid(row= 0, column= 0, sticky="w")
pg1LeftArrowBtn.config(font=("Times New Roman", 20))

tempMonthDate = today.split("/")
stringMonthDate = str(tempMonthDate[1]) + "/" + str(tempMonthDate[2])     #Used to set the intital date on the calendar page

pg1DateLabel = Label(childFrame1, text=stringMonthDate)      #Date selection lable
pg1DateLabel.grid(row= 0, column= 0)
pg1DateLabel.config(font=("Times New Roman", 20))

pg1RightArrowBtn = Button(childFrame1, text=">", command=pg1RightArrowBtnFunc)   #Date selection right arrow
pg1RightArrowBtn.grid(row= 0, column= 0, sticky="e")
pg1RightArrowBtn.config(font=("Times New Roman", 20))

maxDays = calNumDaysForMonthFunc(int(tempMonthDate[1]), int(tempMonthDate[2]))      #Used to get the number of days in the month
createNumCalenderPageBtnsFunc(31)         #Creates the 31 button for the calendar on the calendar page
populateCalendarPageBtnsFunc(maxDays)   #Calls the method responsible for putting the text into the calendar page date buttons
hideCalendarPageBtnsFunc(maxDays)       #Calls the method that is responsible for hiding and unhiding the
                                        #calendar page date buttons depending on the number of days in the month
#---------------------------------------------------------------------------------------------------------------------------------



#ChildFrame2 code ----------------------------------------------------------------------------------------------------------------

def saveMealPlanFunc():     #This function is responsible for adding and removing the required meals from the meal_plan table
    errorWithMealNums = False
    
    for i in range(0, len(imgBtnEntryBoxArray)):
        entryContent = imgBtnEntryBoxArray[i].get()
        
        try:
            if len(entryContent) == 0:      #Stops the entry box from been empty if it is empty then the number 1 is inserted
                imgBtnEntryBoxArray[i].insert(0,"1")
            else:
                temp = int(entryContent)        #Checks the the input in the entry box is just a number and not characters
                
                if temp < 1:        #Stops the entry box from accepting zero and any negative numbers
                    imgBtnEntryBoxArray[i].config(fg="red")
                    errorWithMealNums = True
                else:
                    imgBtnEntryBoxArray[i].config(fg="black")
        except:
            imgBtnEntryBoxArray[i].config(fg="red")     #Runs when what was entered into the entry box isn't just a number
            errorWithMealNums = True

    if errorWithMealNums == False:
        selectedMealArray = []
        
        for i in range(0, len(tickBtnArray)):      #Used to tell which meals have been ticked
            if int(tickBtnArray[i].cget("text")) == 1:
                tempNameFromMealBtn = str(imageBtnsArray[i].cget("text"))       #Gets the meals name from the meals button
                tempNameFromMealBtn = tempNameFromMealBtn.replace("\n", "")      #Removes any break line from the meals name
                tempNameFromMealBtn = tempNameFromMealBtn.strip()       #Removes any trailing white space from the string

                #Uses the index location of the tick button to tell the index of the meal imgBtn so that
                #the id of the meal can be read from the meals table using the name of the meal
                tickedMealID = readDBQuery('SELECT id FROM meals WHERE name = "' + tempNameFromMealBtn + '";')      
                tickedMealID = tickedMealID[0][0]
                selectedMealArray.append(tickedMealID)      #Adds the meal id to the selectedMealArray

        result, amountMeals, date = readMealPlanFunc()

        for z in range(0, len(result)):
            temp = result[z]        #Result is used to store all the ids of the meals that
                                    #are in the meal_plan table for the given date

            try:
                #Removes the meal from the selectedMealArray if it is already in the meal_plan table for that date
                selectedMealArray.remove(int(temp)) 

                entryBoxValue = imgBtnEntryBoxArray[int(temp) - 1].get()        #Gets the number that is in the num meals entry
                                                                                #box for the meal with the id that was just
                                                                                #removed from the selectedMealArray
                if entryBoxValue != amountMeals[0]:     #Checks to see if the num meals in the entry box for the meal is different
                                                        #to the value already in the meal_plan table

                    #Runs if the num meals has changed, so it updates the number to the new value
                    writeDBQuery('UPDATE meal_plan SET amount = ' + entryBoxValue + ' WHERE meal_date = "' + date
                                 + '" AND meal_id = ' + temp)  

                amountMeals = amountMeals[1:]       #Removes the num meals value from the array as the meal that it
                                                    #corresponds to has already been removed from the selectedMealArray
            except ValueError:  #Runs if the id cant be removed from the array as it hasn't been selected
                                #but is in the meal_plan table meaning it needs removing from the table
                writeDBQuery('DELETE FROM meal_plan WHERE meal_date = "' + str(date) + '" AND meal_id = ' + str(temp))

        for x in range(0, len(selectedMealArray)):      #Used to add all the new meals that arn't already in
                                                        #the meal_plan table to the meal_plan table
            numOfMeals = imgBtnEntryBoxArray[(selectedMealArray[x] - 1)].get()
            
            add_meal_plan_query = """
                INSERT INTO meal_plan(meal_date, meal_id, amount)
                VALUES
                ("
                """
            add_meal_plan_query = (add_meal_plan_query + str(date) + '", ' + str(selectedMealArray[x]) + ', '
                                   + str(numOfMeals) + ")")
            writeDBQuery(add_meal_plan_query)

def addNewMealFunc(mealName, mealImageDir):
    global imageBtnsArray
    global tickBtnArray
    global imgBtnEntryBoxArray

    global mealNameArray
    global mealImagesArray


    gridPos = imageBtnsArray[-1].grid_info()        #Used to get the grid position for the last object in the
                                                    #imageBtnsArray so the last meal image btn in the grid
    newRow = 0
    newCol = 0

    if gridPos["column"] > 3:   #This if statement decides the grid location of the newly added meal
        newRow = int(gridPos["row"]) + 1
        newCol = 0
    else:
        newRow = int(gridPos["row"])
        newCol = int(gridPos["column"]) + 1


    mealNameArray.append(str(mealName))     #Adds the new meals name to the golbal array that stores all the meals names
    mealImagesArray.append(str(mealImageDir))   #Add the new meals image directory to the global array
                                                #that stores all the mealls image directories

    temp_open_img = Image.open(str(mealImageDir))   #Opens the image of the newly added meal
    scaled_img = ImageTk.PhotoImage(temp_open_img.resize((353, 199), Image.Resampling.LANCZOS)) #Resizes the image of the newly
                                                                                                #added meal
    #Creates the image btn for the new meal
    tempImgBtn = Button(childFrame2, text=str(mealName), image = scaled_img, compound="top", borderwidth=0,
                        command= lambda: imgBtnClickedFunc(tempImgBtn)) 
    imageBtnsArray.append(tempImgBtn)   #Adds the new meals image btn object to the imageBtnsArray

    tickBtnCreateFunc("0")      #Creates the tick button for the new meal
    mealNumEntryCreateFunc("1") #Creates the entry box for the new meal
    
    imageBtnsArray[-1].grid(row=newRow, column=newCol)     #Places the new meal image button into the grid
    tickBtnArray[-1].grid(row=newRow, column=newCol, sticky="ne")   #Places the new meal tick button into the grid
    imgBtnEntryBoxArray[-1].grid(row=newRow, column=newCol, sticky="ne")    #Places the new meal entry box into the grid

    #This statement is used the read the id of the newly added meal from the meals table
    result = readDBQuery('SELECT id FROM meals WHERE name = "' + str(mealName) + '" AND img_dir = "' + str(mealImageDir) + '";')    
    calMealNutritionalInfoFunc(result[0][0])    #This function is called so that the nutritional information for the
                                                #new meal is calculed and stored int he meal_nutriton table

    resizeFunc()    #This function is called so that the all the widgets for the newly added meal
                    #are added to the grid and resized to the correct size for the windows current width
    

def newMealGuiFunc():       #This function is called when the add new meal button on the calendar page is clicked
    createMealGuiFunc(0,None,None,None,None, None, None)
        

dateBtnArray = []       #Used to store the date selection buttons and the save button

leftArrowBtn = Button(childFrame2, text="<", command=leftArrowBtnFunc)    #Date selection left arrow
dateBtnArray.append(leftArrowBtn)

dateLabel = Label(childFrame2, text=today)      #Date selection lable
dateBtnArray.append(dateLabel)

rightArrowBtn = Button(childFrame2, text=">", command=rightArrowBtnFunc)   #Date selection right arrow
dateBtnArray.append(rightArrowBtn)

addNewMealBtn = Button(childFrame2, text="Add New Meal", command=newMealGuiFunc)    #Add new meal button
dateBtnArray.append(addNewMealBtn)

saveMealsBtn = Button(childFrame2, text="Save Meals", command=saveMealPlanFunc)       #Save meals button
dateBtnArray.append(saveMealsBtn)


openCalendarBtn = Button(childFrame2, text="show calendar", anchor="e", command =openCalendarFunc)      #Show calendar button
openCalendarBtn.grid(row=0, column=1)
openCalendarBtn.config(font=("Times New Roman", 20))
dateBtnArray.append(openCalendarBtn)

def addStandardBtnsFunc():      #This function adds the default buttonts that are always at
                                #the top of childFrame2 before any of the meal buttons
    leftArrowBtn.grid(row= 0, column= 0, sticky="w")
    leftArrowBtn.config(font=("Times New Roman", 20))
    dateLabel.grid(row= 0, column= 0)
    dateLabel.config(font=("Times New Roman", 20))
    rightArrowBtn.grid(row= 0, column= 0, sticky="e")
    rightArrowBtn.config(font=("Times New Roman", 20))
    addNewMealBtn.grid(row=0, column= 3, sticky="e")
    addNewMealBtn.config(font=("Times New Roman", 20))
    saveMealsBtn.grid(row= 0, column= 4, sticky="e", padx=(0,20))
    saveMealsBtn.config(font=("Times New Roman", 20))

addStandardBtnsFunc()
    

imageBtnsArray = []         #Array used to store all of the image buttons so that they can be referenced later on
scaledImgArray = []
tickBtnArray = []
imgBtnEntryBoxArray = []
mealBtnNameLineNumArray = []

img_dir_txt = ""        #Used to store the img directory of the image displayed on
                        #the page that shows the infromation about the meal

def imgBtnClickedFunc(imgBtnObj):
    global CURRENT_CHILD_FRAME
    global img_dir_txt
    global mealClicked

    mealClicked = imgBtnObj
    
    mealId = ""
    mealNameString= str(imgBtnObj.cget("text"))     #Gets the name of the meal from the meals button on the meals page
    mealNameString = mealNameString.strip()         #Removes any trailing white spaces from the string
    mealNameString = mealNameString.replace("\n", "")       #Used to remove any break lines from the meals name

    result = readDBQuery('SELECT id FROM meals WHERE name = "' + mealNameString + '";')
    for row in result:  #This for loop gets the id from the result of the query and stores it in the meadId variable
        mealId = row[0]

    if CURRENT_CHILD_FRAME != 4:
        CURRENT_CHILD_FRAME = 4   #Set so that the corrent child frame is displayed
        
        ingredients_txt, instructions_txt, num_servings_txt, meal_name_txt, img_dir_txt = readMealFromDBFunc(mealId)

        #Calls the function that returns a string that has break lines placed in it,
        #in accordance to the character limit that is passed with the first attribute
        label_instructions = manageCharacterLengthFunc(100, instructions_txt)           
        #label_instructions = instructions_txt
        

        temp_meal_img = Image.open(img_dir_txt)
        scaled_meal_img = ImageTk.PhotoImage(temp_meal_img.resize((565, 318), Image.Resampling.LANCZOS)) #Resizes the image

        mealImageLabel.config(image=scaled_meal_img)
        mealNameLabel.config(text=meal_name_txt)
        mealServingsLabel.config(text="Serves " + num_servings_txt)
        mealIngredientsLabel.config(text="Ingredients \n\n" + ingredients_txt)
        mealInstructionsLabel.config(text="Instructions \n\n" + label_instructions)

        changeMenuFunc()
        changeChildFrameFunc()

        

def imgBtnCreateFunc(imgBtn):   #This function creates the imgBtn's and appends them to the array 
    tempImgBtn = Button(childFrame2, text=(str(mealNameArray[imgBtn])), image = scaledImgArray[imgBtn], compound="top",
                        borderwidth=0, command= lambda: imgBtnClickedFunc(tempImgBtn))
    imageBtnsArray.append(tempImgBtn)
    #The text options sets the text that will be displayed in the button, the image option sets the image that will be displayed
    #in the buuton, the compound option is used to allow us to have both text and an image in the button, and top specifies that
    #we want the image on top of the text, the borderwidth option remove the default styling from the button

#This function opens and scales the image for the meals image button and then
#calls that function that creates the button and passes it the image
def imgBtnCreateImageFunc():    
    #This for loop creates all of the imageButtons that are in childFrame2
    for imageBtn in range(0, len(mealImagesArray)):   #The range of this for loop decides the number of button that are created
        temp_open_img = Image.open(mealImagesArray[imageBtn])   #Opens the image
        scaled_img = ImageTk.PhotoImage(temp_open_img.resize((353, 199), Image.Resampling.LANCZOS)) #Resizes the image
        scaledImgArray.append(scaled_img)

        imgBtnCreateFunc(imageBtn)  #The create imgBtn needs to be created using a seperate function so that the click binding
                                    #for the button is linked to each button object and not just the last button that was created

imgBtnCreateImageFunc()

#This function checks if all of the meals are in the meal_nutrition table and if it
#isn't then it adds the meals nutrition information to the meal_nutrition table
def checkMealNutritionExistsFunc():     
    mealIDsArray = []

    idsRead = readDBQuery('SELECT id FROM meals')       #Reads all the ids of the meals that are in the meals table

    for x in range (0, len(idsRead)):       #Adds the id of each meal to the mealIDsArray
        mealIDsArray.append(idsRead[x][0])
        
    result = readDBQuery('SELECT meal_id FROM meal_nutrition')

    for row in result:
        if int(row[0]) in mealIDsArray:   #Check if the id is in the mealIDsArray and if it is then it removes it
            mealIDsArray.remove(int(row[0]))

    for j in range(0, len(mealIDsArray)):
        calMealNutritionalInfoFunc(mealIDsArray[j])     #Adds the meal nutritional information per servings
                                                        #for the given meal to the meal_nutrition table

checkMealNutritionExistsFunc()

#This function is responsible for reading all the meals that are currently
#in the meal_plan table for the date that is currently in the date label
def readMealPlanFunc():     
    savedMeals = []
    amountMeals = []

    tempDate = dateLabel.cget("text")       #Gets the dame from the dateLabel
    tempDate = tempDate.split("/")

    date = tempDate[2] + "-" + tempDate[1] + "-" + tempDate[0]  #Reorganises the date into the formt yyyy-mm-dd
    
    result = readDBQuery('SELECT meal_id, amount FROM meal_plan WHERE meal_date = "' + str(date) + '"')
    
    for i in range(0, len(result)):
        savedMeals.append(str(result[i][0]))
        amountMeals.append(str(result[i][1]))
        
    return savedMeals, amountMeals, date

def tickBtnClickedFunc(tickBtnObj):
    if int(tickBtnObj.cget("text")) == 0:
        tickBtnObj.config(image= scaled_tick_img2, text= "1")
    else:
        tickBtnObj.config(image= scaled_tick_img1, text= "0")

def tickBtnCreateFunc(tickText):
    tempTickBtn = Button(childFrame2, width=46, height=46, text= tickText, image= scaled_tick_img1, borderwidth=0, bg="black",
                         command= lambda: tickBtnClickedFunc(tempTickBtn))
    tickBtnArray.append(tempTickBtn)

def mealNumEntryCreateFunc(entryText):
    mealEntryBox = Entry(childFrame2, width=3)
    mealEntryBox.insert(0,entryText)
    imgBtnEntryBoxArray.append(mealEntryBox)
    

tickImg1 = Image.open(programImagesDir + r"images\tick_icon_1.jpg")
scaled_tick_img1 = ImageTk.PhotoImage(tickImg1.resize((46, 46), Image.Resampling.LANCZOS))

tickImg2 = Image.open(programImagesDir + r"images\tick_icon_2.jpg")
scaled_tick_img2 = ImageTk.PhotoImage(tickImg2.resize((46, 46), Image.Resampling.LANCZOS))

#This function decides if the tick button has 1 or a 0 in its text arrtibute and then
#calls the tickBtnCreateFunc function to create the tick button
def createInitialTickEntryFunc():
    savedMeals, amountMeals, null = readMealPlanFunc()
    
    for i in range (0, len(imageBtnsArray)):
        tickText = ""
        entryText = ""
        
        try:
            savedMeals.remove(str(i + 1))       #Trys to remove a given id from the array and if it can then it means the meal of
                                                #that id is in the array meaning that it is in the meal_plan table meaning the
                                                #tick button needs to be ticked
            tickText = "1"
            entryText = str(amountMeals[0])
            amountMeals = amountMeals[1:]
        except ValueError:
            tickText = "0"
            entryText = "1"

        tickBtnCreateFunc(tickText)
        mealNumEntryCreateFunc(entryText)

createInitialTickEntryFunc()        #This is called so that all the ticks and entry boxes are setup on intial loading

#This function is responsible for adding the line breaks to the meals
#names so that when they are too long that are on multiple lines
def mealNameLineBreaksFunc():
    global mealBtnNameLineNumArray      #This array is used to store the number of lines for each row of meals so that
                                        #the tick and entry boxes can be adjusted depending on the number of lines
    
    needsLineAdding = False
    z = 0
    for p in range(0, len(imageBtnsArray)):     #Used to check every meal name button that is in the array
        tempButtonName = imageBtnsArray[p].cget("text")     #Gets the name of the meal from the button
        
        #Passes the name to the function that will add the line breaks with the first value passed into the function been the
        #number of characters per line and the second value been the meal name that was read from the button with the retruned
        #string from the function been stored in the tempName variable
        tempName = manageCharacterLengthFunc(25, tempButtonName)
        imageBtnsArray[p]["text"] = tempName    #This line updates the text inside of the meal
                                                #button to the new name with the break lines

        if needsLineAdding != True:     #Stops checking for a break line if it has already been decided
                                        #that the current row will need a break line
            if tempName.count('\n') == 1:   #Checks to see if there is now a break line in the meals name as if there is then a
                                            #break line will need to be added to the end of the single line meal names as
                                            #well so that the buttons stay in line
                needsLineAdding = True

        if z == 4 or p == (len(imageBtnsArray) - 1):    #Used to check every row, this value needs changing
                                                        #if the number of meals per row changes
            if needsLineAdding == True:     #Checks to see if a break line needs adding to the single line meals on this row
                maxBreakLines = 0 #This variable is used to store the highest number of break lines for the given line
                
                for k in range (0, (z + 1)):
                    forTempName = imageBtnsArray[p - k].cget("text")

                    numMealLines = forTempName.count("\n")      #Used to get the number of break lines in the meals name
                    if numMealLines == 0:       #This is statement checks if the meal is a single line and if it is then it
                                                #adds a break line onto the end to make it 2 lines
                        forTempName = forTempName + "\n"
                        imageBtnsArray[p - k]["text"] = forTempName
                    else:
                        if numMealLines > maxBreakLines:
                            maxBreakLines = numMealLines

                needsLineAdding = False
                mealBtnNameLineNumArray.append(maxBreakLines)       #Adds the max number of break lines for a meal
                                                                    #button on the given row to the array
            else:
                mealBtnNameLineNumArray.append(0)       #Adds the value of zero to the array as if it is at this
                                                        #point then every meal on the given row is a single line
            z = 0
        else:
            z = z + 1

#This function is responsible for placing all the imgage buttons, tick buttons and entry boxes into childFrame2 for the meals page 
def placeMealBtnsFunc():    
    #Places the imagesButtons and tickButtons into the childFrame2's grid
    x = 0 #x is used for the starting column number
    n = 1 #n is used for the starting row number
    for i in range(0, len(imageBtnsArray)):
        if x == 5:      #The value in this if statment is set to the number of columns that you want
            x = 0
            n = n + 1
        
        imageBtnsArray[i].grid(row=n, column=x)     #Places the meal image button into the grid
        tickBtnArray[i].grid(row=n, column=x, sticky="ne")
        imgBtnEntryBoxArray[i].grid(row=n, column=x, sticky="ne")
        x = x + 1

    mealNameLineBreaksFunc()

placeMealBtnsFunc()

#---------------------------------------------------------------------------------------------------------------------------------



#ChildFrame3 code ----------------------------------------------------------------------------------------------------------------

def getWeeks(inputDate):    #inputDate should be in the format yyyy/mm This function is responsible for returning the number of
                            #weeks with date ranges for each week taking into account weeks that start before the month and
                            #weeks that end after the end of the month
    
    weeksForMonth = []      #Used to store all the date ranges for the weeks that are calculated

    tempSplit = inputDate.split("/")
    currentMonth = int(tempSplit[1])        #Assigns the passed month to the currentMonth
    currentYear = int(tempSplit[0])         #Assigns the passed year to the currentYear

    #Converts the date input into the datetime type so that it can be used by the datetime class
    inputDateDateType = datetime.strptime(((inputDate + "/01") + " 00:00:00"), '%Y/%m/%d %H:%M:%S')     
    weekDay = int(inputDateDateType.isoweekday())       #Stores an integered depening on the day that the start of
                                                        #the month is with 1 been Monday and 7 been Sunday
    numDaysBack = weekDay - 1

    #Stores the number of days in the month for the given date
    daysCurrentMonth = calNumDaysForMonthFunc(currentMonth, currentYear)    

    #Used to calculate the total number of weeks in the given month
    numWeeks = math.ceil((daysCurrentMonth + numDaysBack) / 7)      


    #This for loop calculates the date range for each week and saves it to the weeksForMonth array
    for i in range(0, numWeeks):        
        startOfWeek = ""        #This string is used to store the beggining date of the week
        endOfWeek = ""          #This string is used to store the ending date of the week
        dayString = ""
        currentYearString = ""
        currentMonthString = ""
        day = 0
        month = currentMonth
        year = currentYear

        if i == 0:      #This runs if it is the first week in the month
            if weekDay != 1:    #This runs if the first day in the month isn't a Monday
                month = month - 1
                if month < 1:   #This if statment prevents the month from been outside the range 1-12
                    month = 12
                    year = year - 1
                    day = calNumDaysForMonthFunc(month, year)
                    day = day - (numDaysBack - 1)
                else:
                    day = calNumDaysForMonthFunc(month, year)       #Get the number of days in the previous month
                    day = day - (numDaysBack - 1)
            else:   #This runs if the first day in the month is a Monday
                day = 1
        else:   #This runs if it isn't the first week in the month
            day = (((i * 7) + 1) - numDaysBack)


        if day < 10:    #This if statement is responsible for formating the day into the format dd
            dayString = "0" + str(day)
        else:
            dayString = str(day)

        if month < 10:      #This if statement is responsible for formatting the month into the format mm
            currentMonthString = "0" + str(month)
            currentYearString = str(year)
        else:
            currentMonthString = str(month)
            currentYearString = str(year)

        #This is where that start date of the week is concatenated into the format dd/mm/yyyy
        startOfWeek = dayString + "/" + currentMonthString + "/" + currentYearString

        if i == 0:  #This if statement is responsible for setting the day for the end of the week
            day = 7 - numDaysBack   #This sets the day that the week ends on taking into account the number of
                                    #days back the week started if the first day in the month wasn't Monday

            if weekDay != 1:    #Checks to see if the month started with a Monday and if it didn't then it
                                #increases the month by 1 as the month will be the previous month
                tempNextMonth = month + 1
                if tempNextMonth < 10:
                    currentMonthString = "0" + str(tempNextMonth)
                else:
                    currentMonthString = str(tempNextMonth)
        else:       #Runs if it isn't the first week in the month
            day = day + 6   #This line sets the day for the end of the week using the
                            #day that we set for the beginning of the week

        if day > daysCurrentMonth:      #Checks that the day isn't large than the number of days in the month
            day = day - daysCurrentMonth    #Calculates how many days into the next month the
                                            #week should and stores it in the day variable

            tempCurrentMonth = currentMonth + 1  #Increases the month by 1 so that the end of the week will be in the next month
            if tempCurrentMonth < 10:       #This if statement is responsible for formatting the month into the format mm
                currentMonthString = "0" + str(tempCurrentMonth)
            elif tempCurrentMonth > 12:     #This if statement prevents the month for going out of range by been larger
                                            #than 12 and instead sets the month to 1 and increases the year by 1 if the
                                            #month is larger than 12
                currentMonthString = "01"
                currentYearString = str(currentYear + 1)
            else:
                currentMonthString = str(tempCurrentMonth)

            
        if day < 10:    #This if statement is responsible for formating the day into the format dd
            dayString = "0" + str(day)
        else:
            dayString = str(day)

        #This is where that end date of the week is concatenated into the format dd/mm/yyyy
        endOfWeek = dayString + "/" + currentMonthString + "/" + currentYearString  

        #This is where the start and end dates of the week are concatenated and then added to the weeksForMonth array
        weeksForMonth.append((startOfWeek + " - " + endOfWeek)) 

    return weeksForMonth

def createWeeksLabels():
    dateSplit = pg3DateLabel.cget("text").split("/")
    date = dateSplit[1] + "/" + dateSplit[0]

    weeksArray = getWeeks(date)
    weeksLabelArray = []

    for i in range(0, len(weeksArray)):
        weekLabel = Label(childFrame3, text="Week " + str(i + 1) + "\n" + str(weeksArray[i]),
                          font=("Times New Roman", 20), justify="left")
        weeksLabelArray.append(weekLabel)


    x = 0 #x is used for the starting column number
    n = 1 #n is used for the starting row number
    for z in range(0, len(weeksLabelArray)):
        if x == 3:      #The value in this if statment is set to the number of columns that you want
            x = 0
            n = n + 1
    
        weeksLabelArray[z].grid(row=n, column=x, padx=5, pady=5)     #Places the meal image button into the grid

        x = x + 1
    
def pg3LeftArrowBtnFunc():
    pg3DateLabelArray = (pg3DateLabel.cget("text")).split("/")

    pg3TempMonth = int(pg3DateLabelArray[0])
    pg3TempYear = int(pg3DateLabelArray[1])

    pg3TempMonth = pg3TempMonth - 1     #Decreases the month by 1

    if pg3TempMonth < 1:
        pg3TempMonth = 12
        pg3TempYear = pg3TempYear - 1 #Decreases the year by 1

    maxDays = calNumDaysForMonthFunc(pg3TempMonth, pg3TempYear)

    pg3TempDay, pg3TempMonth = formatDateFunc(0, pg3TempMonth)

    pg3DateLabel.config(text=str(pg3TempMonth) + "/" + str(pg3TempYear))

    controlWeekFrameVisibilityFunc()    #Controls which week frames are visible
    populateWeeksFunc()     #Calls the function that inserts all the values into each week
    resizeFunc()

def pg3RightArrowBtnFunc():
    pg3DateLabelArray = (pg3DateLabel.cget("text")).split("/")

    pg3TempMonth = int(pg3DateLabelArray[0])
    pg3TempYear = int(pg3DateLabelArray[1])

    pg3TempMonth = pg3TempMonth + 1     #Increases the month by 1

    if pg3TempMonth > 12:
        pg3TempMonth = 1
        pg3TempYear = pg3TempYear + 1 #Increases the year by 1

    maxDays = calNumDaysForMonthFunc(pg3TempMonth, pg3TempYear)

    pg3TempDay, pg3TempMonth = formatDateFunc(0, pg3TempMonth)

    pg3DateLabel.config(text=str(pg3TempMonth) + "/" + str(pg3TempYear))

    controlWeekFrameVisibilityFunc()    #Controls which week frames are visible
    populateWeeksFunc()     #Calls the function that inserts all the values into each week
    resizeFunc()


#All of the images that are used for the icons in the nutritional overview for each week
box_icon_1 = programImagesDir + r"images\rectangle_icon_1.jpg"
box_icon_2 = programImagesDir + r"images\rectangle_icon_2.jpg"
box_icon_3 = programImagesDir + r"images\rectangle_icon_3.jpg"
box_icon_4 = programImagesDir + r"images\rectangle_icon_4.jpg"
box_icon_5 = programImagesDir + r"images\rectangle_icon_5.jpg"

temp_icon_img_1 = Image.open(box_icon_1)
scaled_icon_img_1 = ImageTk.PhotoImage(temp_icon_img_1.resize((15, 15), Image.Resampling.LANCZOS)) #Resizes the image

temp_icon_img_2 = Image.open(box_icon_2)
scaled_icon_img_2 = ImageTk.PhotoImage(temp_icon_img_2.resize((15, 15), Image.Resampling.LANCZOS)) #Resizes the image

temp_icon_img_3 = Image.open(box_icon_3)
scaled_icon_img_3 = ImageTk.PhotoImage(temp_icon_img_3.resize((15, 15), Image.Resampling.LANCZOS)) #Resizes the image

temp_icon_img_4 = Image.open(box_icon_4)
scaled_icon_img_4 = ImageTk.PhotoImage(temp_icon_img_4.resize((15, 15), Image.Resampling.LANCZOS)) #Resizes the image

temp_icon_img_5 = Image.open(box_icon_5)
scaled_icon_img_5 = ImageTk.PhotoImage(temp_icon_img_5.resize((15, 15), Image.Resampling.LANCZOS)) #Resizes the image

#This function decides if the yellow icon should be the decrease or increase version
def checkYellowIncreaseOrDecreaseFunc(tickObj, percentage): 
    if percentage < 100:
        #Yellow Increase
        tickObj.config(image=scaled_icon_img_2, text="2")
    elif percentage > 100:
        #Yellow Decrease
        tickObj.config(image=scaled_icon_img_3, text="3")

#This function decides if the red icon should be the decrease or increase version
def checkRedIncreaseOrDecreaseFunc(tickObj, percentage):        
    if percentage < 100:
        #Red Increase
        tickObj.config(image=scaled_icon_img_4, text="4")
    elif percentage > 100:
        #Red Decrease
        tickObj.config(image=scaled_icon_img_5, text="5")

#This function is responsible for calulating the nutritional values of each week and adding the information to each weeks labels
def populateWeeksFunc():        
    dateStr = str(pg3DateLabel.cget("text"))
    dateSplit = dateStr.split("/")
    dateStr = dateSplit[1] + "/" + dateSplit[0]
    
    weeksArray = getWeeks(dateStr)
    weekTotalsArray = []
    weekTotalsValuesArray = []
    
    for i in range(0, len(weeksArray)):
        weekTotal = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        temp = weeksArray[i]        #Reads the weeks date range from the weeksArray e.g. 29/08/2022 - 04/09/2022
        tempSplit = temp.split("-")
        tempSplit[0] = tempSplit[0].strip()     #Removes any trailing or leading white space
        tempSplit[1] = tempSplit[1].strip()
        date1Split = tempSplit[0].split("/")    #Splits the date up so it can be reorganised from dd/mm/yyyy into
                                                #the format yyyy/mm/dd for the database queries
        date2Split = tempSplit[1].split("/")
        

        date1 = date1Split[2] + "/" + date1Split[1] + "/" + date1Split[0]       #Stores the start date of the week in
                                                                                #the format yyyy/mm/dd
        date2 = date2Split[2] + "/" + date2Split[1] + "/" + date2Split[0]       #Stores the end date of the week in
                                                                                #the format yyyy/mm/dd

        #This query gets all the meals in the meal_plan table for the given date range
        weekIDQueryResult = readDBQuery('SELECT meal_id, amount FROM meal_plan WHERE meal_date BETWEEN "'
                                        + date1 + '" AND "' + date2 + '"')

        mealIDArray = []
        for n in range(0, len(weekIDQueryResult)):  #Adds all of the meal ids that were returned from the query to the
                                                    #mealIDArray taking into account meals that added more than once in a day
            for k in range(0, int(weekIDQueryResult[n][1])):    #Runs for the number of times the meal is in a specific day
                                                                #e.g. 3 of the same meal in one day
                mealIDArray.append(weekIDQueryResult[n][0])

        mealIDArray.sort()  #Sorts the array so that all the same ids are group together
                            #meaning the meals values are calculated more times than needed

        prevMealID = 0
        result = []
        for z in range(0, len(mealIDArray)):    #Calculates the nutritional values off all the ids in the mealIDArray
                                                #and then adds it onto the total nutritional values for the week
            if prevMealID != mealIDArray[z]:    #Checks that the current meal id isn't the same as the one
                                                #that was just previously calculated
                result = readMealNutritionFunc(mealIDArray[z])      #Calls the function that reads the meals nutritonal
                                                                    #values from the meal_nutrition table
                
            for x in range(0, len(weekTotal)):  #Adds each individual values onto the array that stores the total for the week
                weekTotal[x] = weekTotal[x] + result[x]
                
            prevMealID = mealIDArray[z]     #Sets the prevMealID equal to the id of the meal that was just added to the total

        for y in range(0, len(weekTotal)):      #This for loop is responsible for removing an unnecessary zeros from numbers
            if weekTotal[y] != 0:       #Checks that the value isn't simply 0
                temp = str(weekTotal[y]).split(".")
                
                if temp[1] == "0":      #Cheks the value doesn't end in .0 and if it does removes it
                                        #e.g. 0.0 becomes 0 and 50.0 becomes 50
                    weekTotal[y] = int(temp[0])

        weekTotalStringArray = ["Week " + str((i + 1)) + " " + str(tempSplit[0]) + " - " + str(tempSplit[1]),
                                "Calories = " + str(int(weekTotal[0])) + "Kcals",
                                "Fat = " + str(weekTotal[1]) + "g",
                                "Saturated Fat = " + str(weekTotal[2]) + "g",
                                "Carbohydrates = " + str(weekTotal[3]) + "g",
                                "Sugar = " + str(weekTotal[4]) + "g",
                                "Fibre = " + str(weekTotal[5]) + "g",
                                "Protein = " + str(weekTotal[6]) + "g",
                                "Salt = " + str(weekTotal[7]) + "g",
                                "Vitamin A = " + str(weekTotal[8]) + "μg",
                                "Thiamin = " + str(weekTotal[9]) + "mg",
                                "Riboflavin = " + str(weekTotal[10]) + "mg",
                                "Niacin = " + str(weekTotal[11]) + "mg",
                                "Vitamin B6 = " + str(weekTotal[12]) + "mg",
                                "Vitamin B12 = " + str(weekTotal[13]) + "μg",
                                "Vitamin C = " + str(weekTotal[14]) + "mg",
                                "Vitamin D = " + str(weekTotal[15]) + "μg",
                                "Calcium = " + str(weekTotal[16]) + "mg",
                                "Phosphorus = " + str(weekTotal[17]) + "mg",
                                "Magnesium = " + str(weekTotal[18]) + "mg",
                                "Potassium = " + str(weekTotal[19]) + "mg",
                                "Iron = " + str(weekTotal[20]) + "mg",
                                "Zinc = " + str(weekTotal[21]) + "mg",
                                "Copper = " + str(weekTotal[22]) + "mg",
                                "Selenium = " + str(weekTotal[23]) + "μg"]
            
        
        weekTotalsArray.append(weekTotalStringArray)    #Adds the array of the total nutritional value for the week to
                                                        #the overall weekTotalsArray that stores all the array totals
                                                        #for all of the weeks in the given month
        weekTotalsValuesArray.append(weekTotal)

    
    recommendedValues = [[17500,679,217,2331,231,210,392,42,4900,7,9.1,119,9.8,10.5,280,70,4900,3850,2100,24500,60.9,66.5,8.4,525],
                         [14000,546,168,1869,189,210,315,42,4200,5.6,7.7,92.4,8.4,10.5,280,70,4900,3850,1890,24500,103.6,49,8.4,420]]
    
    genderStr = str(genderVar.get())    #Gets the gender that is currently dislayed in the gender dropdown on the analytics page

    for j in range(0, len(weekTotalsArray)):        #This for loops add the values of each nutritional
                                                    #value to the corresponding label of each week

        for k in range (0, len(allWeekLabelsArray[j])):
            allWeekLabelsArray[j][k].config(text=weekTotalsArray[j][k])

        for g in range (0, len(allWeekPercentLabelsArray[j])):
            percentage = 0
            if genderStr == "Male":     #This if statment is used to change the recommend values that are
                                        #used depending on the geneder that has been selected
                percentage = int((weekTotalsValuesArray[j][g] / recommendedValues[0][g]) * 100)
            elif genderStr == "Female":
                percentage = int((weekTotalsValuesArray[j][g] / recommendedValues[1][g]) * 100)
                
            allWeekPercentLabelsArray[j][g].config(text=str(percentage) + " %")

            #This set of if statemenets decides what colour icon should be displayed in the
            #icon label depending on the percentage of recommend that was calculated
            if g == 0 or g == 3:    #Green +-20% Yellow +-40% Red over +-40%        
                if  80 < percentage and percentage < 120:
                    #Green
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                elif 60 < percentage and percentage < 140:
                    checkYellowIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
                else:
                    checkRedIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
            elif g == 5 or g == 6:  #Green +-30% Yellow +-60% Red over +-60%/ over-60% or over 300%
                if 70 < percentage and percentage < 130:
                    #Green
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                else:
                    if g == 5:
                        if 40 < percentage and percentage < 160:     #over +-60%
                            #Yellow
                            checkYellowIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
                        else:
                            #Red
                            checkRedIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
                    elif g == 6:
                        if 40 < percentage and percentage < 300:   #False if over -60% or over +300%
                            #Yellow
                            checkYellowIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
                        else:
                            #Red
                            checkRedIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
            elif g == 1 or g == 2 or g == 4 or g == 7:  #Green less than 80% Yellow 80%-100% Red over 100%
                if 80 > percentage:
                    #Green
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                else:
                    if 100 > percentage:
                        #Yellow Decrease
                        allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_3, text="3")
                    else:
                        #Red Decrease
                        allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_5, text="5")
            elif g == 9 or g == 10 or g == 13:      #Green over 80% Yellow 60%-80% Red less than 60%
                if 80 < percentage:
                    #Green
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                elif 60 < percentage:
                    #Yellow Increase
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_2, text="2")
                else:
                    #Red Increase
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_4, text="4")
            elif g == 17:       #Green 70%-500% Yellow less than 70% greater than 500% Red less than 40% greater than 600%
                if percentage > 70 and percentage < 500:
                    #Green
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                elif percentage > 40 and percentage < 600:
                    #Yellow
                    checkYellowIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
                else:
                    #Red
                    checkRedIncreaseOrDecreaseFunc(allWeekIconLabelsArray[j][g], percentage)
            #Green over 70% Yellow 40%-70% Red less than 40% or more than 200%/300%/1000%/134%
            elif (g == 8 or g == 16 or g == 11 or g == 12 or g == 20 or g == 21 or g == 22
            or g == 23 or g == 14 or g == 15 or g == 18 or g == 19):
                if 40 > percentage:                                                                                                
                    #Red Increase
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_4, text="4")
                elif 70 > percentage:
                    #Yellow Increase
                    allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_2, text="2")
                else:
                    if g == 8 or g == 16:    #200%
                        if 200 < percentage:
                            #Red Decrease
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_5, text="5")
                        else:
                            #Green
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                    elif g == 11 or g == 12 or g == 20 or g == 21 or g == 22 or g == 23:    #300%
                        if 300 < percentage:
                            #Red Decrease
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_5, text="5")
                        else:
                            #Green
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                    elif g == 14 or g == 15:    #1000%
                        if 1000 < percentage:
                            #Red Decrease
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_5, text="5")
                        else:
                            #Green
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")
                    elif g == 18 or g == 19:    #134%
                        if 134 < percentage:
                            #Red Decrease
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_5, text="5")
                        else:
                            #Green
                            allWeekIconLabelsArray[j][g].config(image=scaled_icon_img_1, text="1")


#This function is responsible for controlling which week frames are visible
#depending on how many weeks there are in the given month
def controlWeekFrameVisibilityFunc():       
    dateStr = str(pg3DateLabel.cget("text"))
    dateSplit = dateStr.split("/")
    dateStr = dateSplit[1] + "/" + dateSplit[0]

    weeksArray = getWeeks(dateStr)

    if len(weeksArray) == 5:        #Runs if there are 5 weeks in the month
        weekFrame5.grid(row=3, column=0)
        weekFrame6.grid_forget()
    elif len(weeksArray) == 4:      #Runs if there are 4 weeks in the month
        weekFrame5.grid_forget()
        weekFrame6.grid_forget()
    else:                           #Runs when there is 6 weeks in the month
        weekFrame5.grid(row=3, column=0)
        weekFrame6.grid(row=3, column=1)
            
            
#Each week is store in its own frame this is where all of the frames are created
weekFrame1 = Frame(childFrame3)
weekFrame2 = Frame(childFrame3)
weekFrame3 = Frame(childFrame3)
weekFrame4 = Frame(childFrame3)
weekFrame5 = Frame(childFrame3)
weekFrame6 = Frame(childFrame3)

allWeekLabelsArray = []     #Stores all of the nutritional labels for each week
allWeekPercentLabelsArray = []  #Stores all of the percent labels for each week
allWeekIconLabelsArray = []     #Stores all the icon labels for each week

def createWeekFrames():     #This function is responsible for creating all of the labels for each week frame

    for x in range(0, 6):
        tempArray = []      #This array is used to temporarily store all of the labels
                            #for a week before it is added to the overall allWeekLabelsArray
        tempPercentArray = []
        tempIconArray = []
        
        if x == 0:      #Used to create the name of the week label
            weekNameLabel = Label(weekFrame1, text="Week 1", justify="left", anchor="w", width = 24, font=("Times New Roman", 22))
        elif x == 1:
            weekNameLabel = Label(weekFrame2, text="Week 2", justify="left", anchor="w", width = 24, font=("Times New Roman", 22))
        elif x == 2:
            weekNameLabel = Label(weekFrame3, text="Week 3", justify="left", anchor="w", width = 24, font=("Times New Roman", 22))
        elif x == 3:
            weekNameLabel = Label(weekFrame4, text="Week 4", justify="left", anchor="w", width = 24, font=("Times New Roman", 22))
        elif x == 4:
            weekNameLabel = Label(weekFrame5, text="Week 5", justify="left", anchor="w", width = 24, font=("Times New Roman", 22))
        elif x == 5:
            weekNameLabel = Label(weekFrame6, text="Week 6", justify="left", anchor="w", width = 24, font=("Times New Roman", 22))
    
        weekNameLabel.grid(row=0, column=0, columnspan=4, sticky="w")
        tempArray.append(weekNameLabel)

        column = 0
        for z in range (0, 4):
            for i in range (1, 7):
                if x == 0:      #Used for creating each individual nutrient/vitamin label for each of the weeks
                    mealInfoLabel = Label(weekFrame1, justify="left", anchor="w", width=25, font=("Times New Roman", 12),
                                          borderwidth=1, relief="solid")
                    mealPercentLabel = Label(weekFrame1, justify="right", anchor="e", width=4, font=("Times New Roman", 10))
                    mealIconLabel = Label(weekFrame1, justify="right", anchor="e")
                elif x == 1:
                    mealInfoLabel = Label(weekFrame2, justify="left", anchor="w", width=25, font=("Times New Roman", 12),
                                          borderwidth=1, relief="solid")
                    mealPercentLabel = Label(weekFrame2, justify="right", anchor="e", width=4, font=("Times New Roman", 10))
                    mealIconLabel = Label(weekFrame2, justify="right", anchor="e")
                elif x == 2:
                    mealInfoLabel = Label(weekFrame3, justify="left", anchor="w", width=25, font=("Times New Roman", 12),
                                          borderwidth=1, relief="solid")
                    mealPercentLabel = Label(weekFrame3, justify="right", anchor="e", width=4, font=("Times New Roman", 10))
                    mealIconLabel = Label(weekFrame3, justify="right", anchor="e")
                elif x == 3:
                    mealInfoLabel = Label(weekFrame4, justify="left", anchor="w", width=25, font=("Times New Roman", 12),
                                          borderwidth=1, relief="solid")
                    mealPercentLabel = Label(weekFrame4, justify="right", anchor="e", width=4, font=("Times New Roman", 10))
                    mealIconLabel = Label(weekFrame4, justify="right", anchor="e")
                elif x == 4:
                    mealInfoLabel = Label(weekFrame5, justify="left", anchor="w", width=25, font=("Times New Roman", 12),
                                          borderwidth=1, relief="solid")
                    mealPercentLabel = Label(weekFrame5, justify="right", anchor="e", width=4, font=("Times New Roman", 10))
                    mealIconLabel = Label(weekFrame5, justify="right", anchor="e")
                elif x == 5:
                    mealInfoLabel = Label(weekFrame6, justify="left", anchor="w", width=25, font=("Times New Roman", 12),
                                          borderwidth=1, relief="solid")
                    mealPercentLabel = Label(weekFrame6, justify="right", anchor="e", width=4, font=("Times New Roman", 10))
                    mealIconLabel = Label(weekFrame6, justify="right", anchor="e")
                    
                mealInfoLabel.grid(row=i, column=column, sticky="w")
                tempArray.append(mealInfoLabel)

                mealPercentLabel.grid(row=i, column=column, sticky="e", padx=(0,4))
                tempPercentArray.append(mealPercentLabel)

                mealIconLabel.grid(row=i, column=column, sticky="e", padx=(0,43))
                tempIconArray.append(mealIconLabel)
                
            column = column + 1

            
        allWeekLabelsArray.append(tempArray)
        allWeekPercentLabelsArray.append(tempPercentArray)
        allWeekIconLabelsArray.append(tempIconArray)


    populateWeeksFunc()     #Calls the function that inserts all the values into each week

def pg3SettingsBtnFunc():
    print("Settings")

def genderDropdownCliked(e):    #This function is called when an option is selected in the gender dropdown menu
    populateWeeksFunc()     #Calls the function that will update all the week values


weekFrame1.grid(row=1, column=0, padx=10, pady=10)
weekFrame2.grid(row=1, column=1, padx=10, pady=10)
weekFrame3.grid(row=2, column=0, padx=10, pady=10)
weekFrame4.grid(row=2, column=1, padx=10, pady=10)
weekFrame5.grid(row=3, column=0, padx=10, pady=10)
weekFrame6.grid(row=3, column=1, padx=10, pady=10)
       

pg3LeftArrowBtn = Button(childFrame3, text="<", command=pg3LeftArrowBtnFunc)    #Date selection left arrow
pg3LeftArrowBtn.grid(row= 0, column= 0, sticky="w")
pg3LeftArrowBtn.config(font=("Times New Roman", 20))

tempMonthDate = today.split("/")
stringMonthDate = str(tempMonthDate[1]) + "/" + str(tempMonthDate[2])     #Used to set the intital date on the calendar page

pg3DateLabel = Label(childFrame3, text=stringMonthDate)      #Date selection lable
pg3DateLabel.grid(row= 0, column= 0, sticky="w", padx=(50,0))
pg3DateLabel.config(font=("Times New Roman", 20))

pg3RightArrowBtn = Button(childFrame3, text=">", command=pg3RightArrowBtnFunc)   #Date selection right arrow
pg3RightArrowBtn.grid(row= 0, column= 0, sticky="w", padx=(159,0))
pg3RightArrowBtn.config(font=("Times New Roman", 20))

settings_icon_1 = programImagesDir + r"images/settings_icon.png"
temp_settings_icon_1 = Image.open(settings_icon_1)
scaled_settings_icon_1 = ImageTk.PhotoImage(temp_settings_icon_1.resize((15, 15), Image.Resampling.LANCZOS)) #Resizes the image

pg3SettingsBtn = Button(childFrame3, text="Settings", image=scaled_settings_icon_1, compound="right", borderwidth=0,
                        command=pg3SettingsBtnFunc)
pg3SettingsBtn.grid(row= 0, column= 1, sticky="e", padx=(0,20))

pg3GenderLabel = Label(childFrame3, text="Gender")
pg3GenderLabel.grid(row= 0, column= 0, sticky="w", padx=(220,0))
pg3GenderLabel.config(font=("Times New Roman", 28))

genderVar = StringVar(childFrame3)
genderVar.set("Male")
pg3GenderDropdown = OptionMenu(childFrame3, genderVar, "Male", "Female", command = genderDropdownCliked)
pg3GenderDropdown.grid(row= 0, column= 0, sticky="w", padx=(360,0))
pg3GenderDropdown.config(font=("Times New Roman", 18))

createWeekFrames()
controlWeekFrameVisibilityFunc()
#---------------------------------------------------------------------------------------------------------------------------------



#ChildFrame4 code ----------------------------------------------------------------------------------------------------------------

mealImageLabel = Label(childFrame4)
mealImageLabel.grid(row=0, column=0)

mealNameLabel = Label(childFrame4, justify="left", font=("Times New Roman", 40))
mealNameLabel.grid(row=0, column=1, padx=(20,0), sticky="nw")

mealServingsLabel = Label(childFrame4, justify="left", font=("Times New Roman", 24))
mealServingsLabel.grid(row=0, column=1, padx=(20,0), pady=(70,0), sticky="nw")

mealIngredientsLabel = Label(childFrame4, justify="left", font=("Times New Roman", 20))
mealIngredientsLabel.grid(row=1, column=0, pady=(20,0), sticky="nw")

mealInstructionsLabel = Label(childFrame4, justify="left", font=("Times New Roman", 20))
mealInstructionsLabel.grid(row=1, column=1, pady=(20,0), sticky="nw")
#---------------------------------------------------------------------------------------------------------------------------------

#ChildFrame5 code ----------------------------------------------------------------------------------------------------------------

#All of the widgets for this ChildFrame are added in the function createMealInfoLabel

#---------------------------------------------------------------------------------------------------------------------------------



#scale widgets code---------------------------------------------------------------------------------------------------------------
    
PREV_WIDTH = 0      #Used to store the windows width the last time it was resized
NEED_RESIZE = False     #Used to store a boolean value so that the resize function doesn't get run mulitiple times due to both
                        #the screen changing size and the mouse entering the screen having the potential to the ultimatly
                        #trigger the resize function

#This function is responsible for changing the size of the menu buttons text and
#underlining the text of the button that is currently been displayed
def menuUnderlineFunc(fontSize):        
    global CURRENT_CHILD_FRAME

    if CURRENT_CHILD_FRAME == 1 or CURRENT_CHILD_FRAME == 2 or CURRENT_CHILD_FRAME == 3:
        for i in range (0, len(menuBtnArray)):
            if i == (CURRENT_CHILD_FRAME - 1):      #This if statement controls which menu option
                                                    #in underlined and sets the texts size
                menuBtnArray[i].config(font=("Yu Gothic UI", fontSize, "underline"))
            else:
                menuBtnArray[i].config(font=("Yu Gothic UI", fontSize))
    elif CURRENT_CHILD_FRAME == 4:
        mealMenuBtn1.config(font=("Yu Gothic UI", fontSize))
        mealMenuBtn2.config(font=("Yu Gothic UI", fontSize))
        mealMenuBtn3.config(font=("Yu Gothic UI", fontSize))
    elif CURRENT_CHILD_FRAME == 5:
        calendarMenuBtn1.config(font=("Times New Roman", fontSize))
            
def windowSizeChangeFunc(e):
    global NEED_RESIZE

    resizeBool = checkResizeFunc() #Calls the function to see if the window width has changed

    #This if stement check if the checkResizeFunc has returned True meaning that the widgets do need resizing
    if resizeBool == True:  
        if NEED_RESIZE != True:     #Checks that the NEED_RESIZE variable isn't already true as
                                    #the mouse entering the screen could have already cause it to become true
            NEED_RESIZE = True
        print("Need to resize")

        #Used so that the widgets are resized after half a second if the mouse
        #hasn't already triggered a resize by entering the window
        root.after(600, resizeAfterTimeFunc)   

def resizeAfterTimeFunc():
    global NEED_RESIZE

    #This if statment checks that the NEED_RESIZE variable is still true as the resizing of the widgets could have already been
    #triggered by the mouse entering the scrollbar or canvas meaning that the NEED_RESIZE variable would thus be False as
    #the widgets would no longer need resizing
    if NEED_RESIZE == True: 
        resizeFunc()    

#This function is used to update the Bbox for the scrollbar so that the scroll will
#scroll to the correct location in the yaxis after the widgets have been resized
def updateBbox():
    myCanvas.configure(scrollregion=myCanvas.bbox("all"))
    

def resizeFunc():       #This function is responsible for resizing the widgets to the size of the window
    global NEED_RESIZE  #Needed so that it can be set back to false after resizing the widgets
                        #so that the widgets don't get unnecessarily scaled multiple times
    #global RESIZED #Need to make the image a global variable so that the python garbage collector doesn't clean it up
    global CURRENT_CHILD_FRAME #Used to tell what child frame is currently visible
    global scaled_tick_img1
    global scaled_tick_img2
    global meal_detail_img
    global scaled_icon_img_1
    global scaled_icon_img_2
    global scaled_icon_img_3
    global scaled_icon_img_4
    global scaled_icon_img_5
    global scaled_settings_icon_1
    global mealBtnNameLineNumArray

    canvas_width = myCanvas.winfo_width()    #Stores the current width of the canvas
    scaleValue = (canvas_width / 1903)
        
    size = canvas_width / 40    #Dividing the window widths by 40 gives a good menu font size 
    menuUnderlineFunc(int(size))    #Calls the function that adjustts the text size of the menu buttons in
                                    #accordance with the screen width and underlines the correct buttons text


    if int((canvas_width/38.6)) > 17:     #This if statement scales the x padding of the menu frame
        menuFrame.grid_configure(padx=(int((canvas_width/38.6) - 17),0))

    if int((canvas_width/46)) > 17:       #This if statement scales the x padding of the child frame that is currently visible
        childFrameArray[(CURRENT_CHILD_FRAME - 1)].grid_configure(padx=(int((canvas_width/46) - 17),0))


    #This if statement is responsible for making it so that only the child frame
    #that is currently visible is resized to the window width
    if CURRENT_CHILD_FRAME == 1:  #If true this scales all the widgets on childFrame1 to the window width
        pg1LeftArrowBtn.config(font=("Times New Roman", int(20 * scaleValue)))
        pg1DateLabel.config(font=("Times New Roman", int(20 * scaleValue)))
        pg1RightArrowBtn.config(font=("Times New Roman", int(20 * scaleValue)))

        pg1DateLabelArray = (pg1DateLabel.cget("text")).split("/")   #Gets the current date that is selected on the calendar page
        #Gets the number of days in the selected date so that only the
        #button that should be visible are risized and placed onto the grid
        maxDaysForCalendarPage = calNumDaysForMonthFunc(int(pg1DateLabelArray[0]), int(pg1DateLabelArray[1]))       

        for calendarPgBtnArrayIndex in range (0, int( maxDaysForCalendarPage)):
            calendarPageBtnArray[calendarPgBtnArrayIndex].grid(padx=int(7 * scaleValue), pady=int(10 * scaleValue))
            calendarPageBtnArray[calendarPgBtnArrayIndex].config(font=("Bahnschrift Light", int(19 * scaleValue)))

        
    elif CURRENT_CHILD_FRAME == 2:    #If true this scales all the widgets on childFrame2 to the window width
        if  int(canvas_width/9.64) > 0:       #Used to stop it from trying to scale an image to less than 1px

            for calIndex in range(0, len(dateBtnArray)):        #Adjusts the font size of the date selection buttons
                dateBtnArray[calIndex].config(font=("Times New Roman", int(canvas_width/87.27)))
                        
            scaledImgArray.clear()
            
            
            #Scales the meal buttons and images depending on the screen width
            for i in range(0, len(imageBtnsArray)):
                temp_open_img = Image.open(mealImagesArray[i])   #Opens the image
                scaled_img = ImageTk.PhotoImage(temp_open_img.resize((int(canvas_width/5.43), int(canvas_width/9.64)),
                                                                     Image.Resampling.LANCZOS)) #Resizes the image
                scaledImgArray.append(scaled_img)
                
                
                imageBtnsArray[i].config(width=int(canvas_width/5.43), height=int(canvas_width/8),
                                         font=("Times New Roman", int(canvas_width/87.27)), image=scaledImgArray[i],
                                         padx=int(canvas_width/192), pady=int(canvas_width/63))

                
            tickBtnCounter = 0
            lineBreakArrayIndex = 0
            for tickBtnPlaceIndex in range(0, len(tickBtnArray)):       #This for statment is responsible for adjust
                                                                        #the padding for all of the tick buttons
                if tickBtnCounter == 5:     #This if statement is used to change the index value every line 
                    lineBreakArrayIndex = lineBreakArrayIndex + 1
                    tickBtnCounter = 0

                #Adjusts the x and y padding to adjust to the change in window width
                tickBtnArray[tickBtnPlaceIndex].grid(padx=(18 * scaleValue),
                pady=((27 * scaleValue) - (mealBtnNameLineNumArray[lineBreakArrayIndex] * (16 * scaleValue))))        

                tickBtnCounter = tickBtnCounter + 1

            tickBtnCounter = 0
            lineBreakArrayIndex = 0
            for imgBtnEntryIndex in range(0, len(imgBtnEntryBoxArray)):
                if tickBtnCounter == 5:     #This if statement is used to change the index value every line 
                    lineBreakArrayIndex = lineBreakArrayIndex + 1
                    tickBtnCounter = 0
                
                imgBtnEntryBoxArray[imgBtnEntryIndex].grid(padx=(73 * scaleValue),
                pady=((27 * scaleValue) - (mealBtnNameLineNumArray[lineBreakArrayIndex] * (16 * scaleValue))))
                imgBtnEntryBoxArray[imgBtnEntryIndex].config(font=("Time New Roman", int(14 * scaleValue)))

                tickBtnCounter = tickBtnCounter + 1


            tickBtnSize = int(canvas_width/41.369)      #Sets the size of the tick button and the size
                                                        #of the images used for the tick button
            scaled_tick_img1 = ImageTk.PhotoImage(tickImg1.resize((tickBtnSize, tickBtnSize), Image.Resampling.LANCZOS))
            scaled_tick_img2 = ImageTk.PhotoImage(tickImg2.resize((tickBtnSize, tickBtnSize), Image.Resampling.LANCZOS))
            for tickBtnIndex in range(0, len(tickBtnArray)):
                if int(tickBtnArray[tickBtnIndex].cget("text")) == 0:
                    tickBtnArray[tickBtnIndex].config(width=tickBtnSize, height=tickBtnSize, image=scaled_tick_img1)
                else:
                    tickBtnArray[tickBtnIndex].config(width=tickBtnSize, height=tickBtnSize, image=scaled_tick_img2)
                
    elif CURRENT_CHILD_FRAME == 3:    #If true this scales all the widgets on childFrame3 to the window width
        pg3LeftArrowBtn.config(font=("Times New Roman", int(20 * scaleValue)))
        pg3DateLabel.config(font=("Times New Roman", int(20 * scaleValue)))
        pg3DateLabel.grid(padx=((50 * scaleValue), 0))
        pg3RightArrowBtn.config(font=("Times New Roman", int(20 * scaleValue)))
        pg3RightArrowBtn.grid(padx=((159 * scaleValue), 0))

        scaled_settings_icon_1 = ImageTk.PhotoImage(temp_settings_icon_1.resize((int(40 * scaleValue), int(40 * scaleValue)),
                                                                                Image.Resampling.LANCZOS)) #Resizes the image
        pg3SettingsBtn.config(font=("Times New Roman", int(34 * scaleValue)), image=scaled_settings_icon_1)
        pg3SettingsBtn.grid(padx=(0,int(20 * scaleValue)))

        dateStr = str(pg3DateLabel.cget("text"))
        dateSplit = dateStr.split("/")
        dateStr = dateSplit[1] + "/" + dateSplit[0]

        weeksArray = getWeeks(dateStr)      #Used to get the number of weeks in the given month on the alaytics
                                            #page so that only the weeks that are visible are resized
        numWeeks = len(weeksArray)

        for nutriArrayIndex in range(0, len(allWeekLabelsArray)):   #This for loop resizes the text of each weeks name and
                                                                    #it resizes the text of the nutrition labels for each week
            for nutriIndex in range(0, len(allWeekLabelsArray[nutriArrayIndex])):
                if nutriIndex == 0:
                    allWeekLabelsArray[nutriArrayIndex][nutriIndex].config(font=("Times New Roman", int(24 * scaleValue)))
                else:
                    allWeekLabelsArray[nutriArrayIndex][nutriIndex].config(font=("Times New Roman", int(12 * scaleValue)))

        for percentArrayIndex in range(0, len(allWeekPercentLabelsArray)):      #This for loop resizes the text and padding
                                                                                #of the percentage label for each week
            for percentIndex in range(0, len(allWeekPercentLabelsArray[percentArrayIndex])):
                allWeekPercentLabelsArray[percentArrayIndex][percentIndex].config(font=("Times New Roman", int(9 * scaleValue)))
                allWeekPercentLabelsArray[percentArrayIndex][percentIndex].grid(padx=(0,int(4 * scaleValue)))

        scaled_icon_img_1 = ImageTk.PhotoImage(temp_icon_img_1.resize((int(15 * scaleValue), int(15 * scaleValue)),
                                                                      Image.Resampling.LANCZOS)) #Resizes the image
        scaled_icon_img_2 = ImageTk.PhotoImage(temp_icon_img_2.resize((int(15 * scaleValue), int(15 * scaleValue)),
                                                                      Image.Resampling.LANCZOS)) #Resizes the image
        scaled_icon_img_3 = ImageTk.PhotoImage(temp_icon_img_3.resize((int(15 * scaleValue), int(15 * scaleValue)),
                                                                      Image.Resampling.LANCZOS)) #Resizes the image
        scaled_icon_img_4 = ImageTk.PhotoImage(temp_icon_img_4.resize((int(15 * scaleValue), int(15 * scaleValue)),
                                                                      Image.Resampling.LANCZOS)) #Resizes the image
        scaled_icon_img_5 = ImageTk.PhotoImage(temp_icon_img_5.resize((int(15 * scaleValue), int(15 * scaleValue)),
                                                                      Image.Resampling.LANCZOS)) #Resizes the image

        #This for loop adjusts the padding and the size of the icon for all of the icon labels in each week of the analytics page
        for iconArrayIndex in range(0, numWeeks): 
            for iconIndex in range(0, len(allWeekIconLabelsArray[iconArrayIndex])):
                allWeekIconLabelsArray[iconArrayIndex][iconIndex].grid(padx=(0,int(43 * scaleValue)))

                if int(allWeekIconLabelsArray[iconArrayIndex][iconIndex].cget("text")) == 1:
                    allWeekIconLabelsArray[iconArrayIndex][iconIndex].config(image=scaled_icon_img_1)
                elif int(allWeekIconLabelsArray[iconArrayIndex][iconIndex].cget("text")) == 2:
                    allWeekIconLabelsArray[iconArrayIndex][iconIndex].config(image=scaled_icon_img_2)
                elif int(allWeekIconLabelsArray[iconArrayIndex][iconIndex].cget("text")) == 3:
                    allWeekIconLabelsArray[iconArrayIndex][iconIndex].config(image=scaled_icon_img_3)
                elif int(allWeekIconLabelsArray[iconArrayIndex][iconIndex].cget("text")) == 4:
                    allWeekIconLabelsArray[iconArrayIndex][iconIndex].config(image=scaled_icon_img_4)
                elif int(allWeekIconLabelsArray[iconArrayIndex][iconIndex].cget("text")) == 5:
                    allWeekIconLabelsArray[iconArrayIndex][iconIndex].config(image=scaled_icon_img_5)
            
    elif CURRENT_CHILD_FRAME == 4:
        mealNameLabel.config(font=("Time New Roman", int(40 * scaleValue)))
        mealServingsLabel.config(font=("Time New Roman", int(24 * scaleValue)))
        mealIngredientsLabel.config(font=("Time New Roman", int(20 * scaleValue)))
        mealInstructionsLabel.config(font=("Time New Roman", int(20 * scaleValue)))

        temp_meal_detail_img = Image.open(img_dir_txt)
        meal_detail_img = ImageTk.PhotoImage(temp_meal_detail_img.resize((int(565 * scaleValue), int(318 * scaleValue)),
                                                                         Image.Resampling.LANCZOS)) #Resizes the image
        mealImageLabel.config(image=meal_detail_img)         
    elif CURRENT_CHILD_FRAME == 5:
        for dayNameIndex in range(0, len(calendarDayDetailsName)):
            calendarDayDetailsName[dayNameIndex].config(font=("Times New Roman", int(24 * scaleValue)))

            if dayNameIndex != 0:
                calendarDayDetailsName[dayNameIndex].grid(padx=int(10 * scaleValue), pady=(int(30 * scaleValue),0))

        for dayDetailsIndex in range(0, len(calendarDayDetailsInfo)):
            calendarDayDetailsInfo[dayDetailsIndex].config(font=("Times New Roman", int(16 * scaleValue)))
            calendarDayDetailsInfo[dayDetailsIndex].grid(padx=(int(10 * scaleValue),int(2 * scaleValue)))

    print("Widgets resized")
    

    #Updates the Bbox for the scrollbar after a small time delay so that the changes
    #in widgets dimensions have time to be implimented before the Bbox is updated 
    root.after(200, updateBbox)     
    NEED_RESIZE = False

#Checks the windows previous known width with the current known width so that the widgets arn't resized when they don't need to be
def checkResizeFunc():      
    global PREV_WIDTH
    canvas_width = int(myCanvas.winfo_width())    #Stores the current width of the canvas
    
    if canvas_width > 1:
        if PREV_WIDTH != canvas_width:
            PREV_WIDTH = canvas_width       #Save the canvas width to the PREV_WIDTH variable
            return True

def mouseEnterFunc(e):      #This function is triggered whenever the mouse enters the canvas or scrollbar
    global NEED_RESIZE

    if NEED_RESIZE == True:
        resizeFunc()

def mouseWheelScrolled(e):      #This function is triggered whenever the mouse wheel is scrolled
    sliderLocation = myScrollbar.get()      #Gets the top and bottom locations of the scroll bars slider
    
    if sliderLocation[0] != 0.0 or sliderLocation[1] != 1.0:        #This if stops the yview from been scrolled
                                                                    #when the slider isn't visible on the scrollbar 
        myCanvas.yview_scroll(int(-1*(e.delta/120)), "units")
        
#---------------------------------------------------------------------------------------------------------------------------------



#Event binding code---------------------------------------------------------------------------------------------------------------
        
#Bind the apps configuration so that screen size chnages can be detected
root.bind("<Configure>", windowSizeChangeFunc)  #Event that is triggered when windows changes size
myCanvas.bind("<Enter>", mouseEnterFunc)   #Event that is triggered when the mouse enters the canvas
myScrollbar.bind("<Enter>", mouseEnterFunc)    #Event that is triggered when the mouse enters the scrollbar

root.bind("<MouseWheel>", mouseWheelScrolled)       #Event that is triggered when the mouse wheel is scrolled
#---------------------------------------------------------------------------------------------------------------------------------



#Set the childFrame that is displayed when the window loads ----------------------------------------------------------------------
CURRENT_CHILD_FRAME = 2
changeChildFrameFunc()
#---------------------------------------------------------------------------------------------------------------------------------


root.mainloop()
