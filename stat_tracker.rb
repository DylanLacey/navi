class StatTracker

  def log time, statistic, value
    STDERR.puts "#{time} - #{statistic}:#{value}"
  end
end