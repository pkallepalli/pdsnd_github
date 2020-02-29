import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': r'C:\Users\pkall\OneDrive\Work\Projects\udacity\programing_for_data_science\python\data_files\chicago.csv',
    'new york city': r'C:\Users\pkall\OneDrive\Work\Projects\udacity\programing_for_data_science\python\data_files\new_york_city.csv',
    'washington': r'C:\Users\pkall\OneDrive\Work\Projects\udacity\programing_for_data_science\python\data_files\washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid
    # inputs

    lovCities = ['chicago', 'new york city', 'washington']
    while True:
        try:
            cityIndex = lovCities.index(input(
                'Enter the city to be analyzed (chicago, new york city, washington) : ').lower())
            city = lovCities[cityIndex]
            break
        except Exception as err:
            print('### Exception Occurred: {}'.format(err))

    # TO DO: get user input for month (all, january, february, ... , june)

    lovMonths = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            monthIndex = lovMonths.index(
                input('Enter the month to be analyzed (all, january, february, ... , june) : ').lower())
            month = lovMonths[monthIndex]
            break
        except Exception as err:  # if the try block fails the except is run
            print('### Exception Occurred: {}'.format(err))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    lovDayNames = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
            dayNameIndex = lovDayNames.index(input('Enter the day of the week to be analyzed (all, monday, tuesday, '
                                                   '... sunday) : ').lower())
            day = lovDayNames[dayNameIndex]
            break
        except Exception as err:  # if the try block fails the except is run
            print('### Exception Occurred: {}'.format(err))

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
    #  load data file into a data frame (df)
    df = pd.read_csv(CITY_DATA[city])
    # convert 'Start Time' to datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # adding a month column to data frame (df)
    df['month'] = df['Start Time'].dt.month
    # adding day of ween name to data frame (df)
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filtering the data frame by the selected month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]
    # filtering the data frame by the selected day of the week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Start Hour'].mode()[0]

    print('The most common month is {}'.format(most_common_month))
    print('The most common day of the week is {}'.format(most_common_day_of_week))
    print('The most common start hour is {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + '---->' + df['End Station']
    most_common_trip = df['Trip'].mode()[0]

    print('The most common Start Station is {}'.format(most_common_start_station))
    print('The most common End Station is {}'.format(most_common_end_station))
    print('The most common Trip is {}'.format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Total Travel Time in minutes is {}'.format(total_travel_time / 60))
    print('Mean Travel Time in minutes is {}'.format(mean_travel_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_type = df.groupby(['User Type'])['User Type'].count()
    print('Passengers count by user type is {}'.format(count_user_type))
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        count_gender = df.groupby(['Gender'])['Gender'].count()
        print('Passengers count by gender is {}'.format(count_gender))
    else:
        print('exception: selected city, does not collect passengers gender info')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Gender' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()

        print('Earliest birth year is {}'.format(int(earliest_birth_year)))
        print('Recent birth year is {}'.format(int(recent_birth_year)))
        print('Most common birth year is {}'.format(int(common_birth_year)))
    else:
        print('exception: selected city, does not collect passengers date of birth')

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

        # requesting and viewing raw data(5 lines at a time)
        startIndex, endIndex = 0, 5
        while True:
            raw_data = input('\nWould you like to see next 5 lines of raw data? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break
            else:
                print(df[startIndex:endIndex])
                if endIndex + 5 >= len(df.index):
                    print("\n This is the end of the file, please hit 'no' when prompted.\n")
                else:
                    startIndex += 5
                    endIndex += 5
            continue

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
