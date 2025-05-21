#adding \n at the end of file
echo "" >> "$2"

sed -E 's/([^ ]+)[ ]+([^ ]+)[ ]+([0-9]+)[ ]+([0-9]+)[ ]+([A-Z])[ ]+([^ ]+)[ ]+(.+)/\1,\2,\3,\4,\5,\6,\7/' $2 > tmp_file.csv
sed -E 's/^(E[0-9]*),"/\1,/g; s/\$/\\\$/g; s/"([^\.])$/\1/g; s/\*/\\*/g; s/\+/\\+/g; s/\./\\./g; s/\[/\\[/g; s/\]/\\]/g; s/\{/\\{/g; s/\}/\\}/g; s/\|/\\|/g; s/\(/\\(/g; s/\)/\\)/g; s/\?/\\?/g; s/<\\\*>/[^,]*/g; s/=\[\^,\]\*/=[^ ]*/g; s/Destroying surface Surface\\\(name=\[\^ \]\*\\\) called by \[\^,\]\*/Destroying surface Surface\\\(name=.*\\\) called by .*/; s/visible is \[\^,\]\*/visible is [^, ]*/;' $1 > and_eve.csv
awk '
    BEGIN{
        FS=",";
        OFS=",";
    }
    {
        if (NR==FNR){
            event_temp=substr($0,index($0,",")+1);
            eve_arr[$1]=event_temp;
        }
        else {
            event_mess=substr($0,index($0,$7)-1);
            len=length($0);
            tmp=substr($0,0,len-1);
            printf "%s",tmp;

            for (eve in eve_arr) {
                if (event_mess ~ eve_arr[eve]){
                        printf ",%s",eve;
                }
            }
            print "";
        }
    }
' and_eve.csv tmp_file.csv > default.csv
rm tmp_file.csv and_eve.csv
rm $2