import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s have some fun exploring some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    input1=input('Please select either Chicago, New York City, or Washington: ')
    while input1.upper()!='CHICAGO' and input1.upper()!='NEW YORK CITY' and input1.upper()!='WASHINGTON':
        print('Invalid Response. Please try again')
        input1=input('Please select either Chicago, New York City, or Washington: ')
    city=input1.lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    input2=input("Please select a month between January-June, or 'ALL' for all months: ")
    while input2.upper()!='JANUARY' and input2.upper()!='FEBRUARY' and input2.upper()!='MARCH' and input2.upper()!='APRIL' and input2.upper()!='MAY' and input2.upper()!='JUNE' and input2.upper()!='ALL':
       print('Invalid Response. Please try again')
       input2=input("Please select a month between January-June, or 'All' for all months: ")
    month=input2.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    input3=input("Please select a day of the week (Monday, Tuesday, etc), or 'ALL' for all days: ")
    while input3.upper()!='SUNDAY' and input3.upper()!='MONDAY' and input3.upper()!='TUESDAY' and input3.upper()!='WEDNESDAY' and input3.upper()!='THURSDAY' and input3.upper()!='FRIDAY' and input3.upper()!='SATURDAY' and input3.upper()!='ALL':
        print('Invalid Response. Please try again')
        input3=input("Please select a day of the week (Monday, Tuesday, etc), or 'All' for all days: ")
    day=input3.lower()

    print('-'*40)
    #print(city,month,day)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load file
    df = pd.read_csv(CITY_DATA[city])

    #conver start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week into a new column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter for the correct month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month']==month]

    #filter for the correct day
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mnt=df['month'].mode()[0]
    print('The most common month is ',calendar.month_name[mnt])

    # TO DO: display the most common day of week
    print('The most common day of the week is ',df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    #first need to create hour column
    df['hour'] =df['Start Time'].dt.hour
    print('The most common hour is ',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common start station is ',df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('The most common end station is ',df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    #first need to combine columns to get combinations
    df['combination']=df['Start Station']+' - '+df['End Station']
    print('The most common combination is ',df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total travel time is ',df['Trip Duration'].sum(),' seconds')

    # TO DO: display mean travel time
    print('The mean travel time is ',df['Trip Duration'].mean(),' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Number of users by type:\n',df['User Type'].value_counts().reset_index().to_string(header=None, index=None))

    # TO DO: Display counts of gender
    if ('Gender' in df)==False:
        print('No Gender Data Available')
    else:
        print('\nNumber of users by gender:\n',df['Gender'].value_counts().reset_index().to_string(header=None, index=None))

    # TO DO: Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df)==False:
       print('\nNo Birth Year Data Available')
    else:
        print('\nThe earliest birth year is ',df['Birth Year'].min())
        print('The most recent birth year is ',df['Birth Year'].max())
        print('The most common birth year is ',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #ask the user if they would like to see the raw output of the data
        rawdata=input('\nWould you like to see the raw data for these calculations? Enter yes or no. \n')
        n=5
        while rawdata.lower()=='yes':
            rawout=df.head(n)
            print(rawout)
            rawdata=input('\nWould you like to see more of the raw data? Enter yes or no. \n')
            n+=5


#See if user wants to restart the process
        restart = input('\nWould you like to restart this data project? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
