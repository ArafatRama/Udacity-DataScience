import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). Used a while loop to handle invalid inputs
    while True:
        city = input('the city you are intrested in (chicago, new york city, washington) is: ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Your desired city does not seem to match out our data')
    print(f'\n You have chosen {city.title()} as your city.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('the month you are intrested in (all, january, february, ... , june) is: ').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Your desired month does not seem to match out our data')

    print(f'\n You have chosen {month.title()} as your month.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    while True:
        day = input('the day of the week you are intrested in is: ').lower()
        if day in days:
            break
        else:
            print('Your desired day does not seem to match out our data')
    print(f'\n You have chosen {day.title()} as your day.')

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
    # Loading the data for city
    df = pd.read_csv(CITY_DATA[city])

    # converting the start date from the data
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # exctracting the day and month from the data and start hour, combnation of stations that will be used later on 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour
    df['stations_combinations'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']

    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('the most common month is: {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('the most common day is: {}'.format(common_day_of_week))

    # TO DO: display the most common start hour
    common_start_hour = df['start_hour'].mode()[0]
    print('the most common hour is: {}'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('the most common start station is: {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('the most common end station is: {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    common_combination = df['stations_combinations'].mode()[0]
    print('the most common stations combination is: {}'.format(common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('the total travel time is: {}'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('the total travel time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


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
        print("\nEarliest year of birth:{}, Most recent year of birth:{}, Most common year of birth {}".format(
            most_earliest_year, most_recent_year, most_common_year))
    else:
        print("This city doesn't hold Birth Year data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_rows(df):
    # func to diplay 5 rows each time called
    start_index = 0
    display_data = input(
        "do You want to see rows of the data used to compute the stats? Please write 'yes' or 'no'\n").lower()
    while True:
        if display_data == 'yes':
            print(df.iloc[start_index: start_index + 5])
            start_index = +5
            display_data = input(
                "do You want to see more rows of the data used to compute the stats? Please write 'yes' or 'no'\n").lower()
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()