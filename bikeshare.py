import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
no_lines_of_raw_to_display = 5
def get_raw_data(city):
    """
    :return: dataframes of raw data
    """
    return pd.read_csv(CITY_DATA[city])

def does_user_need_raw_data():
    """
    Ask user if more raw data is to be displayed and returns true if user says 'yes'
    :return: Returns True if user needs to input more data and False otherwise
    """
    raw_data_input_message = "\nDo you want to see next " + str(no_lines_of_raw_to_display) + " lines of raw data? Enter yes or no"
    return get_valid_input(raw_data_input_message, ['yes', 'no']) == 'yes'

def display_raw_data(city):
    """
    Display raw data based on required number of lines
    :param city: City whose details have to be displayed
    """
    raw_data = get_raw_data(city)
    offset = 0
    while does_user_need_raw_data():
        lines_of_data = raw_data[offset: offset + no_lines_of_raw_to_display]
        offset = offset + no_lines_of_raw_to_display
        print(lines_of_data)

def get_valid_input(input_message, valid_items):
    """
    Displays the input_message to user. Obtains input and returns the input value when the input value is in the list of valid_items

    :param input_message: Message to display while taking input from user
    :param valid_items: List of valid items that can be used to validate input from user
    :return: (str) input_item - Item obtained as input from user
    """
    while (True):
        input_item = input(input_message + ": ").lower()
        if input_item in valid_items:
            return input_item
        else:
            print("Invalid input. Please enter one of the following:", valid_items)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_valid_input("Enter the name of the city", list(CITY_DATA.keys()))

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_valid_input("Enter the month name", months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input("Enter the day", days)

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
    df = get_raw_data(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding month number
        month_num = months.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract month and day of week from Start Time to create new columns
    month = df['Start Time'].dt.month
    weekday_name = df['Start Time'].dt.weekday_name
    start_hour = df['Start Time'].dt.hour

    # TO DO: display the most common month
    most_common_month = month.mode()[0]
    print('Most common month is:', most_common_month)

    # TO DO: display the most common day of week
    most_common_day_of_week = weekday_name.mode()[0]
    print('Most common day of week:', most_common_day_of_week)

    # TO DO: display the most common start hour
    common_start_hour = start_hour.mode()[0]
    print('Most common start hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commonly_used_start_station = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station:', commonly_used_start_station)

    # TO DO: display most commonly used end station
    commonly_used_end_station = df['End Station'].value_counts().idxmax()
    print('Most commonly used end station:', commonly_used_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    joining_stations = df['Start Station'] + ", " + df['End Station']
    frequently_used_start_and_stop_station = joining_stations.value_counts().max()
    print('Most frequently used start and stop station is:', frequently_used_start_and_stop_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:')
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year:', earliest_birth_year)

        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year:', most_recent_birth_year)

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most common year of year:', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()