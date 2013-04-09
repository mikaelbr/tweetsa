

var states = {
  'alabama':              'AL',
  'alaska':               'AK',
  'american samoa':       'AS',
  'arizona':              'AZ',
  'arkansas':             'AR',
  'california':           'CA',
  'colorado':             'CO',
  'connecticut':          'CT',
  'delaware':             'DE',
  'dist. of columbia':    'DC',
  'florida':              'FL',
  'georgia':              'GA',
  'guam':                 'GU',
  'hawaii':               'HI',
  'idaho':                'ID',
  'illinois':             'IL',
  'indiana':              'IN',
  'iowa':                 'IA',
  'kansas':               'KS',
  'kentucky':             'KY',
  'louisiana':            'LA',
  'maine':                'ME',
  'maryland':             'MD',
  'marshall islands':     'MH',
  'massachusetts':        'MA',
  'michigan':             'MI',
  'micronesia':           'FM',
  'minnesota':            'MN',
  'mississippi':          'MS',
  'missouri':             'MO',
  'montana':              'MT',
  'nebraska':             'NE',
  'nevada':               'NV',
  'new hampshire':        'NH',
  'new jersey':           'NJ',
  'new mexico':           'NM',
  'new york':             'NY',
  'north carolina':       'NC',
  'north dakota':         'ND',
  'northern marianas':    'MP',
  'ohio':                 'OH',
  'oklahoma':             'OK',
  'oregon':               'OR',
  'palau':                'PW',
  'pennsylvania':         'PA',
  'puerto rico':          'PR',
  'rhode island':         'RI',
  'south carolina':       'SC',
  'south dakota':         'SD',
  'tennessee':            'TN',
  'texas':                'TX',
  'utah':                 'UT',
  'vermont':              'VT',
  'virginia':             'VA',
  'virgin islands':       'VI',
  'washington':           'WA',
  'west virginia':        'WV',
  'wisconsin':            'WI',
  'wyoming':              'WY'
}


module.exports.generateStateCode = function (stateName) {
  if (!states[stateName.toLowerCase()]) {
    return false;
  }

  return states[stateName.toLowerCase()];
};