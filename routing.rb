require 'sinatra'
require_relative './stat_tracker'

tracker = StatTracker.new


get '/frank-says' do
  'Put this in your pipe & smoke it!'
end

post '/stat/:name' do |name|
  #logger.debug "Logging #{n}"
  tracker.log params['time'], 'active', params['active']
  tracker.log params['time'], 'free', params['free']
  tracker.log params['time'], 'total', params['total']
  200
end
