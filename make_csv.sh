sed -E 's/\[(.+)\] \[(notice|error)\] (.+)/\1,\2,\3/' $1 > file1.csv

awk '
    BEGIN{
        FS=","
        OFS=","
        e1="jk2_init() Found child <*> in scoreboard slot <*>"
        e2="workerEnv.init() ok <*>"
        e3="mod_jk child workerEnv in error state <*>"
        e4="[client <*>] Directory index forbidden by rule: <*>"
        e5="jk2_init() Can'\''t find child <*> in scoreboard"
        e6="mod_jk child init <*> <*>"
    }
    /jk2_init\(\) Found child .* in scoreboard slot .*/{
        len=length($0)
        tmp=substr($0,0,len-1)
        print tmp,"E1",e1
    }
    /workerEnv\.init\(\) ok .*/{
        len=length($0)
        tmp=substr($0,0,len-1)
        print tmp,"E2",e2   
    }
    /mod_jk child workerEnv in error state .*/{
        len=length($0)
        tmp=substr($0,0,len-1)
        print tmp,"E3",e3
    }
    /\[client .*\] Directory index forbidden by rule: .*/{
        len=length($0)
        tmp=substr($0,0,len-1) 
        print tmp,"E4",e4
    }
    /jk2_init\(\) Can'\''t find child .* in scoreboard/{
        len=length($0)
        tmp=substr($0,0,len-1)
        print tmp,"E5",e5
    }
    /mod_jk child init .* .*/{
        len=length($0)
        tmp=substr($0,0,len-1)
        print tmp,"E6",e6
    }
    ' file1.csv > default.csv
    rm $1 
    rm file1.csv