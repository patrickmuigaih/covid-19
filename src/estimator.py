import random


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

    return int(infections*15/100)


def hospital_beds_by_time(beds_count, infections):
    available_beds = int(beds_count * 90/100)
    covid_beds = int(available_beds * 35/100)

    return covid_beds - infections


def icu_request_by_time(infections):
    return int(infections * 5/100)


def ventilators_request_by_time(infections):
    return int(infections * 2/100)

def dollars_in_flight(infections, avg_daily_income, time_to_elapse, period_type='days'):

    if period_type == 'weeks':
        time_to_elapse = time_to_elapse * 7
    if period_type == 'months':
        time_to_elapse = time_to_elapse * 30

    return (infections * 0.65) * avg_daily_income * time_to_elapse


def estimator(data):
    impact = dict()
    severeImpact = dict()

    reportedCases = data['reportedCases']

    # get currentily infected
    infected_count = currently_infected(reportedCases, type='impact')
    severe_infected_count = currently_infected(reportedCases, type='severe')
    impact['currentlyInfected'] = infected_count
    severeImpact['currentlyInfected'] = severe_infected_count

    # compute infectionsByRequestedTime
    infections_count = infections_by_time(
        infected_count, data['timeToElapse'], data['periodType'])
    severe_infections_count = infections_by_time(
        severe_infected_count, data['timeToElapse'], data['periodType'])
    impact['infectionsByRequestedTime'] = infections_count
    severeImpact['infectionsByRequestedTime'] = severe_infections_count

    # compute severeCasesByRequestedTime
    positive_impact_cases = severe_cases_by_time(infected_count)
    positive_severe_cases = severe_cases_by_time(severe_infections_count)
    impact['severeCasesByRequestedTime'] = positive_impact_cases
    severeImpact['severeCasesByRequestedTime'] = positive_severe_cases

    # compute hospitalBedsByRequestedTime
    impact_beds = hospital_beds_by_time(
        data['totalHospitalBeds'], positive_impact_cases)
    severe_beds = hospital_beds_by_time(
        data['totalHospitalBeds'], positive_severe_cases)
    impact['hospitalBedsByRequestedTime'] = impact_beds
    severeImpact['hospitalBedsByRequestedTime'] = severe_beds

    # casesForICUByRequestedTime
    impact['casesForICUByRequestedTime'] = icu_request_by_time(
        positive_impact_cases)
    severeImpact['casesForICUByRequestedTime'] = icu_request_by_time(
        positive_severe_cases)

    # casesForVentilatorsByRequestedTime
    impact['casesForVentilatorsByRequestedTime'] = ventilators_request_by_time(
        positive_impact_cases)
    severeImpact['casesForVentilatorsByRequestedTime'] = ventilators_request_by_time(
        positive_severe_cases)

    # compute dollarsInFlight
    avg_income = data['region']['avgDailyIncomeInUSD']
    impact['dollarsInFlight'] = dollars_in_flight(
        impact['infectionsByRequestedTime'], avg_income, data['timeToElapse'], data['periodType'])
    severeImpact['dollarsInFlight'] = dollars_in_flight(
        severeImpact['infectionsByRequestedTime'], avg_income, data['timeToElapse'], data['periodType'])

    output = dict(data=data, impact=impact, severeImpact=severeImpact)
    return output
