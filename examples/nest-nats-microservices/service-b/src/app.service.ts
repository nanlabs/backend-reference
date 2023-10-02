import { Injectable } from '@nestjs/common';
import { Resource1Created } from './incomingEvents/Resource1Created.event';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello World!';
  }

  handleResource1Created(data: Resource1Created) {
    console.log('handled data:', data);
  }
}
