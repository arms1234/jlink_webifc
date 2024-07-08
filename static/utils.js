

function is_digit(d) 
{
    for(i = 0; i < d.value.length; i++)
    {
		ch = d.value.charAt(i);
		if(ch < '0' || ch > '9') 
        {
			apprise('This field have illegal characters, must be [ 0 - 9 ]');
            d.value = d.defaultValue;
			return false;
		}
	}

	return true;
}



function check_range(d, min, max, field_name) 
{
	is_digit(d);

	dd = parseInt(d.value, 10);	
	if ( !(dd <= max && dd >= min) ) 
    {		
		apprise(field_name +' value is out of range ['+ min + ' - ' + max +']');
		d.value = d.defaultValue;		
	} else 
		d.value = dd;	
}


function read_from_fields(id_pref, field_num)
{
    var v = new Array(field_num);
    for(i = 0; i < field_num; i++)
        v[i] = $("#"+id_pref+"_"+i).val();
    return v;
}


function check_ip(ip, name)
{
	if(ip[0] == "0" && ip[1] == "0" && ip[2] == "0" && ip[3] == "0")
    {		
        apprise(name+' value is incorrect!');
		return false;		
	}

	if((ip[0] != "0" || ip[1] != "0" || ip[2] != "0") && ip[3] == "0")
    {
        apprise(name+' value is incorrect!');
		return false;
	}

    return true;
}

function check_netmask(mask, name)
{
    var match0 = -1;
	var match1 = -1;
    var m = new Array(4);

	if(mask[0] == "0" && mask[1] == "0" && mask[2] == "0" && mask[3] == "0")
    {		
        apprise(name+' value is incorrect!');
		return false;		
	}

	if((mask[0] != "255" || mask[1] != "255" || mask[2] != "255") && mask[3] == "255")
    {
        apprise(name+' value is incorrect!');
		return false;
	}


    for(i = 3; i >= 0; i--)
        m[i] = mask[i];
        for(j = 1; j <= 8; j++)
        {
            if((m[i] % 2) == 0)   
                match0 = (3-i)*8 + j;
            else if(((m[i] % 2) == 1) && match1 == -1)   
                match1 = (3-i)*8 + j;
            m[i] = Math.floor(m[i] / 2);
        }

    if(match0 > match1)
    {
        apprise(name+' value is incorrect!');
        return false;
    }

    return true;
}


function check_gateway(gw, ip, mask)
{
	if(gw[0] == "0" && gw[1] == "0" && gw[2] == "0" && gw[3] == "0")
    {		
        apprise('Gateway address value is incorrect!');
		return false;		
	}

	if((gw[0] != "0" || gw[1] != "0" || gw[2] != "0") && gw[3] == "0")
    {
        apprise('Gateway address value is incorrect!');
		return false;
	}

    for(i = 0; i < 4; i++)
        if((ip[i] & mask[i]) != (gw[i] & mask[i]))
        {
			apprise("IP address and gateway is not at same subnet mask!");
			return false;
		}


    return true;
}

function addr_to_str(addr)
{
    var str;
    str = addr[0] + ".";
    str += addr[1] + ".";
    str += addr[2] + ".";
    str += addr[3];

    return str;
}

