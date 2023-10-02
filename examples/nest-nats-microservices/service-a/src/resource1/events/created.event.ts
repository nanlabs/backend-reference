import { CreateResource1Dto } from '../dto/create-resource1.dto';

export const PATTERN = 'resource_1_created';

export class Resource1Created {
  public readonly pattern = PATTERN;
  public readonly v: number = 1;
  constructor(public readonly data: CreateResource1Dto) {}
}
