import webapp2 #import basic mainpage - look up to understand better
import datecheck #import other module that contains validation
import escape # import module that escapes html

# time to create a variable that creates the html to be shown
form =""" 
<form method="post">
    What is Your Birthday?
    <br>
    <label>Month <input type="text" name="month" value="%(month)s"></label>
    <label>Day <input type="text" name="day" value="%(day)s"></label>
    <label>Year <input type="text" name="year" value="%(year)s"></label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

#create foundational class
class MainPage(webapp2.RequestHandler):
    #method to write the page - created because the main page would be re-rendered multiple times depending on whether there are errors or not 
    #escape functions in dictionary escape_html function so that an errored form return doesn't apply the html tag formatting and screw up thepage
    def write_form(self, error="", month="", day="", year=""): 
        self.response.out.write(form % {"error": error,
                                        "month": escape.escape_html(month), 
                                        "day": escape.escape_html(day),
                                        "year": escape.escape_html(year)})
    #this used to be the main self.response.out.write(form), but changed when write_form was created   
    def get(self):
        self.write_form()
    #this method allows the user to enter and send info to be checked - or just sent if no validation was used        
    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
    # these run the entered info through the datecheck module - then spits them back out    
        month = datecheck.valid_month(user_month)
        day = datecheck.valid_day(user_day)
        year = datecheck.valid_year(user_year)
    # checking to see if the entered info passes the validation tests of module datecheck    
        if not (month and day and year):
            self.write_form("Oops! Invalid entry. Please enter a valid date.",
                            user_month, user_day, user_year)
            
        else:
            self.redirect("/thanks") # this says - everything passes, so go to the thanks page (and thus the ThanksHandler)
            
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid date.")

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', ThanksHandler)], debug=True)
