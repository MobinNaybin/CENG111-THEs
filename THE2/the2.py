def check_month(month_calendar):
    cost = 0
    rulestate = check_rule(month_calendar)  # rulechecker function

    if len(rulestate) != 0:
        return rulestate
    else:
        currentindex = 0
        numn = 0  # number of neighbor
        for i in month_calendar:
            currentindex += 1

            # Rule1 Cost
            if i == "m":
                cost += 10

            # Rule2 Cost
            elif i == "f":
                cost += 20

            # Rule3 Cost
            elif i == "b":
                cost += 30
                if (currentindex % 5) == 0:
                    try:
                        if month_calendar[currentindex] == "b":
                            cost += 60
                            continue
                    except:
                        continue
                elif (currentindex % 5) == 4:
                    continue
                elif (currentindex % 5) == 3:
                    try:
                        if (
                            month_calendar[currentindex + 1] == "b"
                            and month_calendar[currentindex] != "b"
                        ):
                            cost += 30
                    except:
                        continue
                try:  # can be chagned
                    if (
                        (currentindex % 5) != 0
                        and (currentindex % 5) != 4
                        and (currentindex % 5) != 3
                        and month_calendar[currentindex + 1] == "b"
                    ):
                        if month_calendar[currentindex] == "b":
                            continue
                        else:
                            cost += 30
                            continue
                except:
                    continue
                try:
                    if (
                        (currentindex % 5) != 0
                        and (currentindex % 5) != 4
                        and (currentindex % 5) != 3
                        and month_calendar[currentindex + 2] == "b"
                    ):
                        if (
                            month_calendar[currentindex + 1] == "b"
                            and month_calendar[currentindex] == "b"
                        ):
                            continue
                        elif (
                            month_calendar[currentindex + 1] == "b"
                            or month_calendar[currentindex] == "b"
                        ):
                            continue
                        else:
                            cost += 60
                            continue
                except:
                    continue

            # Rule4 Cost
            elif i == "g":
                cost += 50
                continue

            # Rule5 Cost
            elif i == "a1":
                cost += 32
                continue

            # Rule6 Cost
            elif i == "a2":
                cost += 27
                continue

            # Rule7 Cost
            elif i == "n":
                numn += 1
                if numn > 1:
                    cost += 5 ** (numn - 1)
                    continue

        return cost


def check_rule(month_calendar):
    errorlist = []
    numf = 0  # number of father
    numg = 0  # number of grandma on wednesday
    currentindex = 0  # starts from 1
    for i in month_calendar:
        currentindex += 1
        # Rule1
        if i == "m":
            motherindex = (month_calendar.index("m") + 1) % 5
            if (currentindex % 5) != motherindex:
                errorlist.append(1)

        # Rule2
        elif i == "f":
            numf += 1
            if numf > 2:  # cehck if there is more than 2 times
                errorlist.append(2)
            elif (
                currentindex % 5
            ) == 0:  # check if its on friday to pass checking the next day
                continue
            try:
                if month_calendar[currentindex] == "f":  # check consecutivity
                    errorlist.append(2)
            except:
                continue

        # Rule4
        elif i == "g":
            if (currentindex % 5) == 3:
                numg += 1
            if numg > 1:
                errorlist.append(4)

        # Rule5
        elif i == "a1":
            if (currentindex % 5) == 2 or (currentindex % 5) == 0:
                continue
            else:
                errorlist.append(5)

        # Rule6
        elif i == "a2":
            if (currentindex % 5) == 1:
                continue
            elif month_calendar[currentindex - 2] == "a1":
                errorlist.append(6)

        # Rule7
        elif i == "n":
            if (
                (currentindex % 5) == 1
                or (currentindex % 5) == 2
                or (currentindex % 5) == 3
            ):
                continue
            else:
                errorlist.append(7)

    return list(set(errorlist))
