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

post '/stat/:name' do |name|
  case name do
  when "memory"
    #logger.debug "Logging #{n}"
    tracker.log params['time'], 'active', params['active']
    tracker.log params['time'], 'free', params['free']
    tracker.log params['time'], 'total', params['total']
    200
  when "ping"
    tracker.log params['time'], 'ping result', params['result']
    200
  end 
end
