import random
import math


def currently_infected(reported_count, type='severe'):
    # calculate currently infected
    if type == 'severe':
        return reported_count * 50
    else:
        return reported_count * 10


def infections_by_time(infected_count, time_to_elapse, period_type='days'):
    """
    To estimate the number of infected people 30 days from now,
    note that infected_count doublesevery 3 days
    so you'd have to multiply it by a factor of 2
    E.g: infected_count x (2 to the power of *factor*) where factor is 10 for a 30 day
    duration (there are 10 sets of 3 days in a perioid of 30 days)
    """

    if period_type == 'weeks':
        time_to_elapse = time_to_elapse * 7
    if period_type == 'months':
        time_to_elapse = time_to_elapse * 30

    return infected_count * (2**(time_to_elapse//3))


def severe_cases_by_time(infections):
    """
    This is the estimated number of severe positive
    cases that will require hospitalization to recover.
    """
    return (infections*15/100.0)


def hospital_beds_by_time(beds_count, infections):
    available_beds = (beds_count * 35/100.0)
    beds = available_beds - infections
    if beds > 0:
        return math.floor(beds)
    return math.ceil(beds)


def icu_request_by_time(infections):
    return int(infections * 5/100)


def ventilators_request_by_time(infections):
    return int(infections * 2/100)


def dollars_in_flight(infections, avg_income_population, avg_daily_income, time_to_elapse, period_type='days'):
    if period_type == 'weeks':
        time_to_elapse = time_to_elapse * 7
    if period_type == 'months':
        time_to_elapse = time_to_elapse * 30
    return (infections * avg_income_population/100) * avg_daily_income


def estimator(data):
    impact = dict()
    severeImpact = dict()

    reportedCases = data['reportedCases']

    # get currentily infected
    impact['currentlyInfected'] = currently_infected(
        reportedCases, type='impact')
    severeImpact['currentlyInfected'] = currently_infected(
        reportedCases, type='severe')

    # compute infectionsByRequestedTime
    impact['infectionsByRequestedTime'] = infections_by_time(
        impact['currentlyInfected'], data['timeToElapse'], data['periodType'])
    severeImpact['infectionsByRequestedTime'] = infections_by_time(
        severeImpact['currentlyInfected'], data['timeToElapse'], data['periodType'])

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
    avg_income = data['region']['avgDailyIncomeInUSD']
    avg_income_population = data['region']['avgDailyIncomePopulation']
    impact['dollarsInFlight'] = dollars_in_flight(
        impact['infectionsByRequestedTime'], avg_income_population, avg_income, data['timeToElapse'], data['periodType'])
    severeImpact['dollarsInFlight'] = dollars_in_flight(
        severeImpact['infectionsByRequestedTime'], avg_income_population, avg_income, data['timeToElapse'], data['periodType'])

    output = dict(data=data, impact=impact, severeImpact=severeImpact)
    return output
