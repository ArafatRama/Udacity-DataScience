import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Avoid Repetition in get_filters Function
def get_user_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        else:
            print("Invalid input. Please try again.")
     
# create a helper function to print statistics, reducing repetition
def print_stat(stat_name, stat_value):
    print(f'The most common {stat_name} is: {stat_value}')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
  
    city = get_user_input('the city you are interested in (chicago, new york city, washington) is: ', CITY_DATA.keys())
    print(f'\nYou have chosen {city.title()} as your city.')

    month = get_user_input('the month you are interested in (all, january, february, ... , june) is: ',
                           ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    print(f'\nYou have chosen {month.title()} as your month.')

    day = get_user_input('the day of the week you are interested in is: ',
                         ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
    print(f'\nYou have chosen {day.title()} as your day.')

    print('-' * 40)
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
    #Loading the data for city
    df = pd.read_csv(CITY_DATA[city])
        
    #converting the start date from the data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #exctracting the day and month from the data and start hour, combnation of stations that will be used later on 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour
    df['stations_combination']='from '+ df['Start Station'] + ' to ' + df['End Station']

    
    # Filter by month
    if month != 'all':
        months= ['january', 'february', 'march', 'april', 'may', 'june']
        month=months.index(month)+1
        df = df[df['month'] == month ]

    #Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print_stat('month', common_month)


    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print_stat('day_of_week', common_day_of_week)

    # TO DO: display the most common start hour
    common_start_hour = df['start_hour'].mode()[0]
    print_stat('start_hour', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print_stat('Start Station', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print_stat('End Station', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    common_combination = df['stations_combination'].mode()[0]
    print_stat('stations_combination', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('the total travel time is: {}'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('the average travel time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('the amount of users for each type is as follows:\n {}'.format(user_type))

    # TO DO: Display counts of gender
    if city in ['chicago', 'new york city']:
          gender_type = df['Gender'].value_counts()
          print('the amount of users form each gender is as follows:\n {}'.format(gender_type))
    else:
        print("This city doesn't hold gender data")
                

    # TO DO: Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city']:
        most_earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth:{}, Most recent year of birth:{}, Most common year of birth {}".format(most_earliest_year,most_recent_year,most_common_year))
    else:
        print("This city doesn't hold Birth Year data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rows(df):
    # func to diplay 5 rows each time called
    start_index= 0
    display_data = input("do You want to see rows of the data used to compute the stats? Please write 'yes' or 'no'\n").lower()
    while True:
        if display_data == 'yes':
            print(df.iloc[start_index : start_index+5])
            start_index += 5
            display_data = input("do You want to see more rows of the data used to compute the stats? Please write 'yes' or 'no'\n").lower()
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()