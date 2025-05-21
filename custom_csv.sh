min=$1
max=$2

awk -v min="$min" -v max="$max" '
    BEGIN{   
        FS = ",";
        mon_dict["Jan"] = "01";
        mon_dict["Feb"] = "02";
        mon_dict["Mar"] = "03";
        mon_dict["Apr"] = "04";
        mon_dict["May"] = "05";
        mon_dict["Jun"] = "06";
        mon_dict["Jul"] = "07";
        mon_dict["Aug"] = "08";
        mon_dict["Sep"] = "09";
        mon_dict["Oct"] = "10";
        mon_dict["Nov"] = "11";
        mon_dict["Dec"] = "12";
            }
    function get_date_list(time, list, a ,tim){
            split(time, a, " ");
            list[1] = a[5];
            list[2] = mon_dict[a[2]];
            list[3] = a[3];
            split(a[4],tim,":");
            list[4] = tim[1];
            list[5] = tim[2];
            list[6] = tim[3];
        }
        function time_compare(t1, t2, list_t1, list_t2, i){

            get_date_list(t1, list_t1);
            get_date_list(t2, list_t2);
            for(i=1;i<=6;i++){
                if(list_t1[i] > list_t2[i]){
                    return 1;
                }
                else if(list_t1[i] < list_t2[i]){
                    return 0;
                }
            }
            return 1;
        }

        {
         if (time_compare($1, min) && time_compare(max, $1)) {
            print $0;
        }
    }
' default.csv > custom.csv