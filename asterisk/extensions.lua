first_group = {"200",}
second_group = {"202","204"}

function make_dial_string(sip_array)
	sips_string = ""
	for i = 1, #sip_array do
		sips_string = (sips_string .. "SIP/" .. sip_array[i])
		if i < #sip_array then
			sips_string = (sips_string .. "&")
		end
	end
	return sips_string
end

extensions = {}
extensions.internal = {}

extensions.internal["_XXX"] = function(c, e)
	app.answer()
	app.ringing()
	app.dial("SIP/" .. e)
end
 
extensions.internal["666"] = function(c, e)
	app.set("__DYNAMIC_FEATURES=opendoor")
	app.answer()
	app.ringing()
  -- Dial first group
	app.dial(make_dial_string(first_group) .. ",20,g")
	
	if channel["DIALSTATUS"]:get() == "NOANSWER" then
		app.dial(make_dial_string(first_group) .. "&" .. make_dial_string(second_group))
	end
end
