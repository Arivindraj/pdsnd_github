import time
import pandas as pd
import numpy as np

# loading files
CITY_DATA = {
    'chicago':'chicago.csv',
    'new york city':'new_york_city.csv',
    'washington':'washington.csv'
}

def get_city():
    '''
    This function starts the user interface by introduction and
    asking the user with the city he/she wants to analyze
    '''
    print('Hello! Let\'s explore some US bikeshare data!')
    print(' ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('We currently have data for the cities listed below:')
    print('Chicago ')
    print('New York ')
    print('Washington')
    print(' ')
    city = input('Which city would you like to explore ? Please type the name of the city  ')
    city = city.lower()
    # handling unexpected input by user
    while True:     
            if city == 'chicago':
                print("\n Cool! You have selected Chicago City!\n")
                return 'chicago'
            if city == 'new york':
                print("\n Cool! You have selected New York City!\n")
                return 'new york city'
            elif city == 'washington':
                print("\n Cool! You have selected Washington! \n")
                return 'washington'
            else:
                print('\n Please enter the name of cities provided above\n')
                city = input('Which city would you like to explore ? ')
                city = city.lower()
    return city

def get_filter():
    
    period_filter = input('\nWould you like to filter the data by month, day of the month, day of the week, or not at all? Please type "no" if you prefer not at all.\n')
    period_filter = period_filter.lower()

    while True: 
        if period_filter == "month":
            while True:
                day_month = input("\nDo you want to filter the data by day of the month ? Please type 'YES' or 'NO'\n").lower()
                if day_month == "no":
                    print('\n The data is now being filtered by month...\n')
                    return 'month'
                elif day_month == "yes":
                   print ('\n The data is now being filtered by month and day of the month...\n')
                   return 'day_of_month'
                
        if period_filter == "day":
            print('\n The data is now being filtered by the day of the week...\n')
            return 'day_of_week'
        elif period_filter == "no":
            print('\n No period filter is being applied to the data\n')
            return "none"
        period_filter = input("\n Please choose a period filter option between 'month', 'day' of the week, or none (no) \n").lower()
# get user input for month (all, january, february, ... , june)
def month_info(m):      
    if m == 'month':
        month = input('\nChoose month! January, February, March, April, May, or June? Please type the full month name.\n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June? Please type the full month name.\n')
        return month.strip().lower()
    else:
        return 'none'
# Asks the user for a month and a day of month,
def month_day_info(df, day_m):     
    month_day = []
    if day_m == "day_of_month":
        month = month_info("month")
        month_day.append(month)
        maximum_day_month = max_day_month(df, month)

        while (True):
            ask = """ \n Which day of the month? \n
            Please type your response as an integer between 1 and 7 """                 
            ask  = ask + str(maximum_day_month) + "\n" 
            day_m = input(ask)

            try: 
                day_m = int(day_m)
                if 1 <= day_m <= maximum_day_month:
                    month_day.append(day_m)
                    return month_day
            except ValueError:
                print("That's not a numeric value")
    else:
        return 'none'
 # Asking the user to select specified day    
def day_info(d):      
    if d == 'day_of_week':
        day = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        while day.lower().strip() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease type a day as a choice from M, Tu, W, Th, F, Sa, Su. \n')
        return day.lower().strip()
    else:
        return 'none'

def load_data(city):
    # Loads data for the specified city
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    return df

def time_filters(df, time, month, week_day, md):
    '''
    Filters the data according to the criteria specified by the user.
    Local Variables:
    df         - city dataframe 
    time       - indicates the specified time (either "month", "day_of_month", or "day_of_week")
    month      - indicates the month used to filter the data
    week_day   - indicates the week day used to filter the data
    md         - list that indicates the month (at index [0]) used to filter the data
                    and the day number (at index [1])
    Result:
    df - dataframe to be used for final calculation
    '''
    #Filter by Month
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = md[1]
        df = df[df['day_of_month'] == day]

    return df

def max_day_month(df, month):
    '''Gets the max day of the month '''

    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]
    max_day = max(df["day_of_month"])
    return max_day

# display the most common month
def month_freq(df):
    print('\n Which is the most the most common month ?\n')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

# display the most common day of week
def day_freq(df): 
    print('\n  What is the most common day of the week ?\n')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

# display the most common start hour  
def hour_freq(df):
    print('\n What is the most common start hour for bike rides?\n')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]
    
def trip_duration(df):
    
    print('\n What is the total travel time & mean travel time ?\n')
    # display total travel time
    trip_duration = df['Trip Duration'].sum()
    print('Total trip duration: ', trip_duration)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel time: ', mean_travel_time)

def stations_freq(df):
    # display most commonly used start station  
    print("\n What is the most commonly used start station?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)

    # display most commonly used end station
    print("\n What is the most commonly used end station?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def common_trip(df):
    # display most frequent combination of start station and end station trip
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n What was the most frequent combination of start station and end station trip?\n')
    return result

def bike_users(df):
    # Display counts of user types
    print('\n Counts of user types\n')
    return df['User Type'].value_counts()

def birth_years(df):
    # Display earliest, most recent, and most common year of birth

    print('\n What is the earliest, most recent, and most common year of birth?\n')

    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest year of birth is: ', earliest_birth_year)
    else:
        print('Birth year information is not available for this city')
     
    if 'Birth Year' in df:
        recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year: ', recent_birth_year)
    else:
        print('Birth year information is not available for this city')

    if 'Birth Year' in df:
        common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year: ', common_birth_year)
    else:
        print('Birth year information is not availabe for this city')

def gender_data(df):
     # Display counts of gender
    try:
        print('\n What is the breakdown of gender among riders?\n')
        return df['Gender'].value_counts()
    except:
        print('There is no gender data in the source.')
    
def process(f, df):
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def disp_raw_data(df):
    '''
    Displays the data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns: 
       none
    '''
    df = df.drop(['month', 'day_of_month'], axis = 1)
    row_index = 0

    see_data = input("\nYou like to see rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\n Would you like to see five more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()

def main():
    
    city = get_city()
    df = load_data(city)
    period_filter = get_filter()
    month = month_info(period_filter)
    day = day_info(period_filter)
    month_day = month_day_info(df, period_filter)

    df = time_filters(df, period_filter, month, day, month_day)
    disp_raw_data(df)
    
    apply_countdown = [month_freq,
     day_freq, hour_freq, 
     trip_duration, common_trip, 
     stations_freq, bike_users, birth_years, gender_data]
	
    # displays processing time for each function block
    for x in apply_countdown:	
        process(x, df)

    # Restarting option
    restart = input("\n Would you like to restart? Type \'yes\' or \'no\'.\n")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        main()

if __name__ == '__main__':
    main()