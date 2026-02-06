class Diet_service:
    def __init__(self,user):
        self.user=user 

    def bmi(self):
        return self.user.weight/(self.user.height**2 ) 
    
    def calories(self):
        if self.user.goal.lower()=="maintain":
            return self.user.weight*32
        elif self.user.goal.lower()=="cut":
            return self.user.weight*28 
        elif self.user.goal.lower()=="bulk":
            return self.user.weight*36 
        
    def protein(self):
        if self.user.goal.lower()=="maintain":
            return self.user.weight*1.6
        elif self.user.goal.lower()=="cut":
            return self.user.weight*2.2
        elif self.user.goal.lower()=="bulk":
            return self.user.weight*1.8 
        

    def diet_chart(self):
        if self.user.goal.lower()=="cut":
            return {
                "breakfast":["Oats 50g + Milk", "2 egg white and 1 whole egg"],
                "lunch":["Rice 150g", "Chicken breast 150g", "Salad"],
                "Snacks":["Curd 200g", "One seasonal fruit"],
                "dinner":["Roti(2 piece)", "paneer 100g/chicken breast 100g", "vegetables"]
            }
        elif self.user.goal.lower()=="bulk":
            return {
                "breakfast":["Oats 100g + Milk", "4 whole eggs", "3 banana"],
                "lunch":["Rice 250g", "Chicken 200g", "Dal", "boiled potato(2 piece)", "curd 150g"],
                "snacks":["Banana shake", "curd 100g", "Peanut butter", "2 whole eggs"],
                "dinner":["Roti(3 piece)", "paneer/chicken 150g", "Vegetables"]

            }
        

        else:
            return {
                "breakfast":["Oats 80g + Milk", "3 whole eggs", "2 banana"],
                "lunch":["Rice 200g", "Chicken 100g", "Dal"],
                "snacks":["Fruits", "cards", "1 whole egg"],
                "dinner":["Roti(3 piece)", "Paneer/chicken 100g", "Dal"]
            }
        


        