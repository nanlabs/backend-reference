import { PartialType } from '@nestjs/mapped-types';
import { CreateResource1Dto } from './create-resource1.dto';

export class UpdateResource1Dto extends PartialType(CreateResource1Dto) {}
