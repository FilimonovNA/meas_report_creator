from const import NEMO_POSTFIX_LENGTH


def main(meas_list):
    depend_user_nemo_names = {}
    for meas in meas_list:
        slave_number = get_number_slave(meas)
        user_meas_name = get_user_meas_name(meas, len(slave_number))
        meas_name_for_join = get_meas_name_for_join(user_meas_name, slave_number)
        depend_user_nemo_names[meas] = meas_name_for_join
    joins_dict = get_joins_dict(depend_user_nemo_names)

    return joins_dict


def get_user_meas_name(meas_name, len_slave_number):
    user_name = meas_name[:-NEMO_POSTFIX_LENGTH-len_slave_number]
    return user_name


def get_number_slave(meas_name):
    if meas_name[-6] in ['.', ':']:
        slave_number = meas_name[-5:]
    elif meas_name.endswith('.mrk'):
        return 'mrk'
    else:
        slave_number = meas_name[-6:]
    return slave_number


def get_meas_name_for_join(user_meas_name, slave_number):
    return user_meas_name + '.' + slave_number


def get_joins_dict(depend_user_nemo_names):
    set_joins = set(depend_user_nemo_names.values())
    joins_dict = {}
    for join_name in set_joins:
        one_join_meas = []
        for nemo_meas, user_name in depend_user_nemo_names.items():
            if user_name == join_name:
                one_join_meas.append(nemo_meas)
        if joins_dict.get(join_name) is None:
            joins_dict[join_name] = one_join_meas
    return joins_dict
