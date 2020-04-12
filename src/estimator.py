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
    impact['infectionsByRequestedTime'] = infections_by_time(
        infected_count, data['timeToElapse'], data['periodType'])
    severeImpact['infectionsByRequestedTime'] = infections_by_time(
        severe_infected_count, data['timeToElapse'], data['periodType'])

    return dict(data=data, impact=impact, severeImpact=severeImpact)
