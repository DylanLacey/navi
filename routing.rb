require 'sinatra'
require_relative './stat_tracker'

tracker = StatTracker.new


get '/' do
  'Navi is a tiny stat tracker of no real utility.'
end

get '/memory_script.py' do
  location = File.join Dir.pwd, 'logstats.py'
  return [200, File.read(location)]
end

get '/ping_script.py' do
  location = File.join Dir.pwd, 'logping.py'
  return [200, File.read(location)]
end

get '/trace_script.py' do
  location = File.join Dir.pwd, 'logtrace.py'
  return [200, File.read(location)]
end

post '/stat/:name' do |stat_name|
  if stat_name == "memory"
    #logger.debug "Logging #{n}"
    tracker.log params['time'], 'active', params['active']
    tracker.log params['time'], 'free', params['free']
    tracker.log params['time'], 'total', params['total']
    200
  elsif stat_name == "ping"
    tracker.log params['time'], 'ping result', params['result']
    200
  elsif stat_name == "log"
    tracker.log params['time'], "log_message", params['message']
  elsif stat_name == "domain"
    param_lines = params['route_data'].split('\n')
    param_lines.each do |line|
      tracker.log params['time'], "trace", line
    end
    200
  else

  end 
end
