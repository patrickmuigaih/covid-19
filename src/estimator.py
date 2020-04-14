
import math

def to_days(time_to_elapse, period_type):
    if period_type == 'weeks':
        return time_to_elapse * 7
    elif period_type == 'months':
        return time_to_elapse * 30
    else:
        return time_to_elapse


def currently_infected(reported_count, type='severe'):
    # calculate currently infected
    if type == 'severe':
        return reported_count * 50
    else:
        return reported_count * 10


def infections_by_time(infected_count, days):
    """
    To estimate the number of infected people 30 days from now,
    note that infected_count doublesevery 3 days
    so you'd have to multiply it by a factor of 2
    E.g: infected_count x (2 to the power of *factor*) where factor is 10 for a 30 day
    duration (there are 10 sets of 3 days in a perioid of 30 days)
    """

    return infected_count * (2**(days//3))

def severe_cases_by_time(infections):
    """
    This is the estimated number of severe positive
    cases that will require hospitalization to recover.
    """
    return (infections * (15/100.0))


def hospital_beds_by_time(beds_count, infections):
    available_beds = (beds_count * (35/100.0))
    beds = available_beds - infections
    if beds > 0:
        return math.floor(beds)
    return math.ceil(beds)


def icu_request_by_time(infections):
    return int(infections * (5/100))


def ventilators_request_by_time(infections):
    return int(infections * (2/100))


def dollars_in_flight(infections, avg_daily_income_population, avg_daily_income, days):
    return int(infections * avg_daily_income_population * avg_daily_income / days)


def estimator(data):
    impact = dict()
    severeImpact = dict()

    days = to_days(data['timeToElapse'], data['periodType'], )
    reportedCases = data['reportedCases']

    # get currentily infected
    impact['currentlyInfected'] = currently_infected(
        reportedCases, type='impact')
    severeImpact['currentlyInfected'] = currently_infected(
        reportedCases, type='severe')

    # compute infectionsByRequestedTime
    impact['infectionsByRequestedTime'] = infections_by_time(
        impact['currentlyInfected'], days)
    severeImpact['infectionsByRequestedTime'] = infections_by_time(
        severeImpact['currentlyInfected'], days)

    # compute severeCasesByRequestedTime
    impact['severeCasesByRequestedTime'] = severe_cases_by_time(
        impact['infectionsByRequestedTime'])
    severeImpact['severeCasesByRequestedTime'] = severe_cases_by_time(
        severeImpact['infectionsByRequestedTime'])

    # compute hospitalBedsByRequestedTime
    impact['hospitalBedsByRequestedTime'] = hospital_beds_by_time(
        data['totalHospitalBeds'], impact['severeCasesByRequestedTime'])
    severeImpact['hospitalBedsByRequestedTime'] = hospital_beds_by_time(
        data['totalHospitalBeds'], severeImpact['severeCasesByRequestedTime'])

    # casesForICUByRequestedTime
    impact['casesForICUByRequestedTime'] = icu_request_by_time(
        impact['infectionsByRequestedTime'])
    severeImpact['casesForICUByRequestedTime'] = icu_request_by_time(
        severeImpact['infectionsByRequestedTime'])

    # casesForVentilatorsByRequestedTime
    impact['casesForVentilatorsByRequestedTime'] = ventilators_request_by_time(
        impact['infectionsByRequestedTime'])
    severeImpact['casesForVentilatorsByRequestedTime'] = ventilators_request_by_time(
        severeImpact['infectionsByRequestedTime'])

    # compute dollarsInFlight
    impact['dollarsInFlight'] = dollars_in_flight(
        impact['infectionsByRequestedTime'], data['region']['avgDailyIncomePopulation'], data['region']['avgDailyIncomeInUSD'], days)
    severeImpact['dollarsInFlight'] = dollars_in_flight(
        severeImpact['infectionsByRequestedTime'], data['region']['avgDailyIncomePopulation'], data['region']['avgDailyIncomeInUSD'], days)

    output = dict(data=data, impact=impact, severeImpact=severeImpact)
    return output
