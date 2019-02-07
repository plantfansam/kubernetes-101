import React from 'react'

import Pod from './Pod.jsx'
import ConfigMap from './ConfigMap.jsx'
import Secret from './Secret.jsx'
import Ingress from './Ingress.jsx'
import ReplicationController from './ReplicationController.jsx'
import Service from './Service.jsx'
import Volume from './Volume.jsx'
import Job from './Job.jsx'

export default class App extends React.Component {
  render() {
    return (
      <div>
        <nav>
          <h1>⚡🎸 This thing's on! 🎤⚡</h1>
        </nav>
        <div>
          <Pod/>
          <Service />
          <ConfigMap />
          <Secret />
          <Ingress />
          <ReplicationController />
          <Volume />
          <Job />
        </div>
      </div>
    );
  }
}
