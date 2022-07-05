function function_name -> (parameter1,parameter2,RVal) {
    return_flag = 0;
    extpy print("start");
    break_flag = 0;
    while (1 and ((!break_flag) and (!return_flag))) {
        if (parameter1==0) then {
            if (parameter2==0) then {
                RVal = 0;
                return_flag = 1
            }
            else {
                empty
            };
            if ((!return_flag)) then {
                extpy print("statement1");
                break_flag = 1
            }
            else {
                empty
            }
        }
        else {
            empty
        };
        if ((!break_flag) and (!return_flag)) then {
            extpy print("statement2");
            break_flag = 1
        }
        else {
            empty
        }
    };
    break_flag = 0;
    if ((!return_flag)) then {
        if (parameter1==0) then {
            break_flag = 0;
            while (1 and (!break_flag)) {
                break_flag = 0;
                for(count=0;count<5 and !break_flag;count=count+1) {
                    continue_flag = 0;
                    if (count<=2) then {
                        if (count==0) then {
                            extpy print("statement3");
                            continue_flag = 1
                        }
                        else {
                            empty
                        };
                        if ((!continue_flag)) then {
                            if (count==1) then {
                                extpy print("statement4");
                                continue_flag = 1
                            }
                            else {
                                extpy print("statement5")
                            };
                            if ((!continue_flag)) then {
                                if (count==2) then {
                                    extpy print("statement6");
                                    break_flag = 1
                                }
                                else {
                                    empty
                                };
                                if ((!break_flag)) then {
                                    extpy print("statement7")
                                }
                                else {
                                    empty
                                }
                            }
                            else {
                                empty
                            }
                        }
                        else {
                            empty
                        }
                    }
                    else {
                        extpy print("statement8")
                    };
                    if ((!continue_flag) and (!break_flag)) then {
                        extpy print("statement9")
                    }
                    else {
                        empty
                    }
                };
                if ((!break_flag)) then {
                    extpy print("statement10")
                }
                else {
                    empty
                };
                break_flag = 0;
                if (parameter1==0) then {
                    extpy print("statement11");
                    break_flag = 1
                }
                else {
                    empty
                };
                if ((!break_flag)) then {
                    extpy print("statement12");
                    break_flag = 1
                }
                else {
                    empty
                }
            };
            if ((!break_flag)) then {
                extpy print("statement13")
            }
            else {
                empty
            };
            break_flag = 0;
            extpy print("statement14");
            RVal = 1;
            return_flag = 1
        }
        else {
            empty
        };
        if ((!return_flag)) then {
            extpy print("end");
            RVal = (-1);
            return_flag = 1
        }
        else {
            empty
        }
    }
    else {
        empty
    }
};
frame(ret,RVal) and (
ret = function_name(0,0,RVal);
extpy print("First return value = ",ret);
ret = function_name(0,1,RVal);
extpy print("Second return value = ",ret)
)
